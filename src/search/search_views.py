import time
import httpx
import requests
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from .models import Currency
from src.base.services import get_isfavorite


class SearchView(APIView):
    authlogin = settings.AUTHLOGIN
    authpass = settings.AUTHPASS

    def get_search_result(self, query_params):
        search_url = (
            f"http://tourvisor.ru/xml/search.php?format=json"
            f"&authlogin={self.authlogin}&authpass={self.authpass}"
        )

        for param, value in query_params.items():
            search_url += f"&{param}={value}"

        requestid = requests.get(search_url)

        if requestid.status_code != 200:
            return Response({"response": False})

        try:
            return requestid.json()["result"]["requestid"]
        except KeyError:
            return Response({"response": False})

    def get(self, request):
        query_params = request.query_params

        currency = query_params.get("currency")

        # Если юзер выбрал СОМ
        if currency == "99":
            mutable_query_params = query_params.copy()
            usd_exchange = Currency.objects.get(currency="USD").purchase
            eur_exchange = Currency.objects.get(currency="EUR").purchase

            pricefrom = int(query_params.get("pricefrom"))
            priceto = int(query_params.get("priceto"))

            mutable_query_params["pricefrom"] = pricefrom / usd_exchange
            mutable_query_params["priceto"] = priceto / usd_exchange
            mutable_query_params["currency"] = "1"

            requestid = self.get_search_result(mutable_query_params)

            time.sleep(6)

            url = (
                f"http://tourvisor.ru/xml/result.php?format=json&requestid={requestid}"
                f"&authlogin={self.authlogin}&authpass={self.authpass}"
            )

            response = requests.get(url)
            if response.status_code != 200:
                return Response({"response": False})

            data = response.json()
            for hotel in data["data"]["result"]["hotel"]:
                if hotel["currency"] == "USD":
                    hotel["currency"] = hotel["currency"] = "KGS"
                    hotel["price"] = int(hotel["price"] * usd_exchange)

                    for tour in hotel["tours"]["tour"]:
                        if tour["currency"] == "USD":
                            tour["currency"] = "KGS"
                            tour["price"] = int(tour["price"] * usd_exchange)
                        else:
                            tour["currency"] = "KGS"
                            tour["price"] = int(tour["price"] * eur_exchange)

                elif hotel["currency"] == "EUR":
                    hotel["currency"] = hotel["currency"] = "KGS"
                    hotel["price"] = int(hotel["price"] * eur_exchange)

                    for tour in hotel["tours"]["tour"]:
                        if tour["currency"] == "USD":
                            tour["currency"] = "KGS"
                            tour["price"] = int(tour["price"] * usd_exchange)
                        else:
                            tour["currency"] = "KGS"
                            tour["price"] = int(tour["price"] * eur_exchange)

            return Response(data)

        else:
            requestid = self.get_search_result(query_params)

            time.sleep(6)

            url = (
                f"http://tourvisor.ru/xml/result.php?format=json&requestid={requestid}"
                f"&authlogin={self.authlogin}&authpass={self.authpass}"
            )

            response = requests.get(url)

        if response.status_code != 200:
            return Response({"response": False})
        return Response(response.json())


class FilterParams(APIView):
    def get(self, request):
        authlogin = settings.AUTHLOGIN
        authpass = settings.AUTHPASS

        options = requests.get(
            f"http://tourvisor.ru/xml/list.php?type="
            f"hotel,country,departure,meal,stars,operator"
            f"&format=json&authpass={authpass}&authlogin={authlogin}"
        )
        options_data = options.json()

        services_operators = requests.get(
            f"http://tourvisor.ru/xml/list.php?authlogin={authlogin}&authpass={authpass}"
            f"&format=json&type=services,operator"
        ).json()["lists"]

        if options.status_code != 200:
            return Response({"response": False})

        options_data["lists"]["services"] = services_operators["services"]
        options_data["lists"]["operators"] = services_operators["operators"]

        return Response(options_data)


class FilterHotels(APIView):
    def get(self, request):
        authlogin = settings.AUTHLOGIN
        authpass = settings.AUTHPASS

        hotcountry = request.query_params.get("hotcountry")
        hotregion = request.query_params.get("hotregion")
        hotstars = request.query_params.get("hotstars")
        hotrating = request.query_params.get("hotrating")
        hotactive = request.query_params.get("hotactive")
        hotrelax = request.query_params.get("hotrelax")
        hotfamily = request.query_params.get("hotfamily")
        hothealth = request.query_params.get("hothealth")
        hotcity = request.query_params.get("hotcity")
        hotbeach = request.query_params.get("hotbeach")
        hotdeluxe = request.query_params.get("hotdeluxe")

        url = "http://tourvisor.ru/xml/list.php?type=hotel&format=json"
        url += f"&authpass={authpass}&authlogin={authlogin}"

        if hotcountry:
            url += f"&hotcountry={hotcountry}"
            
        if hotregion:
            url += f"&hotregion={hotregion}"

        if hotstars:
            url += f"&hotstars={hotstars}"

        if hotactive:
            url += f"&hotactive={hotactive}"

        if hotrating:
            url += f"&hotrating={hotrating}"

        if hotfamily:
            url += f"&hotfamily={hotfamily}"

        if hothealth:
            url += f"&hothealth={hothealth}"

        if hotcity:
            url += f"&hotcity={hotcity}"

        if hotbeach:
            url += f"&hotbeach={hotbeach}"

        if hotdeluxe:
            url += f"&hotdeluxe={hotdeluxe}"
        
        if hotrelax:
            url += f"&hotrelax={hotrelax}"

        hotels = requests.get(url)

        if hotels.status_code != 200:
            return Response({"response": False})
        return Response(hotels.json())


class FilterCountries(APIView):
    def update_country_name(self, country):
        if country.get("name") == "Киргизия":
            country["name"] = "Кыргызстан"
        return country

    def get(self, request, departureid):
        authlogin = settings.AUTHLOGIN
        authpass = settings.AUTHPASS

        countries = requests.get(
            f"http://tourvisor.ru/xml/list.php?type=country&cndep={departureid}"
            f"&format=json&authpass={authpass}&authlogin={authlogin}"
        )
        if countries.status_code != 200:
            return Response({"response": False})

        countries = countries.json()

        for i in countries["lists"]["countries"]["country"]:
            if i["name"] == "Киргизия":
                i["name"] = "Кыргызстан"
                break

        return Response(countries)


class RegCountryView(APIView):
    def get(self, request, regcountry):
        authlogin = settings.AUTHLOGIN
        authpass = settings.AUTHPASS

        regions = requests.get(
            f"http://tourvisor.ru/xml/list.php?type=region,subregion&regcountry={regcountry}"
            f"&authlogin={authlogin}&authpass={authpass}"
        )

        if regions.status_code != 200:
            return Response({"response": False})
        return Response(regions.json())


class TourActualizeView(APIView):
    def get(self, request, tourid):
        authlogin = settings.AUTHLOGIN
        authpass = settings.AUTHPASS

        actualize = requests.get(
            f"http://tourvisor.ru/xml/actualize.php?tourid={tourid}&request=0"
            f"&format=json&authpass={authpass}&authlogin={authlogin}"
        )

        if actualize.status_code != 200:
            return Response({"response": False})
        return Response(actualize.json()["data"])


class TourActdetailView(APIView):
    def get(self, request, tourid):
        authlogin = settings.AUTHLOGIN
        authpass = settings.AUTHPASS

        actualize = requests.get(
            f"http://tourvisor.ru/xml/actdetail.php?tourid={tourid}"
            f"&format=json&authpass={authpass}&authlogin={authlogin}"
        )
        if actualize.status_code != 200:
            return Response({"response": False})
        return Response(actualize.json())


class HotelDetailView(APIView):
    def get(self, request, hotelcode):
        authlogin = settings.AUTHLOGIN
        authpass = settings.AUTHPASS

        hoteldetail = requests.get(
            f"http://tourvisor.ru/xml/hotel.php?hotelcode={hotelcode}"
            f"&format=json&authpass={authpass}&authlogin={authlogin}&reviews=1"
        )

        if hoteldetail.status_code != 200:
            return Response({"response": False})
        return Response(hoteldetail.json()["data"])


class HotToursListView(APIView):
    def get(self, request):
        authlogin = settings.AUTHLOGIN
        authpass = settings.AUTHPASS

        hottours = requests.get(
            f"http://tourvisor.ru/xml/hottours.php?city=80&city2=60&items=20&picturetype=1"
            f"&format=json&authpass={authpass}&authlogin={authlogin}&reviews=1"
        )

        if hottours.status_code != 200:
            return Response({"response": False})
        return Response(hottours.json())


class TourDetailView(APIView):
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, tourid):
        authlogin = settings.AUTHLOGIN
        authpass = settings.AUTHPASS
        user = request.user

        # Get hotelcode to return hotel detail
        try:
            tour = requests.get(
                f"http://tourvisor.ru/xml/actualize.php?tourid={tourid}&request=1"
                f"&format=json&authpass={authpass}&authlogin={authlogin}"
            )

            if tour.status_code != 200:
                return Response({"response": False})
        except KeyError:
            return Response({"reponse": False})

        # try:
        #     hoteldetail = requests.get(
        #         f"http://tourvisor.ru/xml/hotel.php?hotelcode={tour.json()['data']['tour']['hotelcode']}"
        #         f"&format=json&authpass={authpass}&authlogin={authlogin}&reviews=1"
        #     )

        #     if hoteldetail.status_code != 200:
        #         return Response({"response": False})
        # except KeyError:
        #     return Response({"reponse": False})

        # Get flights on this tour
        try:
            flights = requests.get(
                f"http://tourvisor.ru/xml/actdetail.php?tourid={tourid}"
                f"&format=json&authpass={authpass}&authlogin={authlogin}"
            )
            if flights.status_code != 200:
                return Response({"response": False})
            flights = flights.json()["flights"]
        except KeyError:
            flights = flights.json()

        if user.is_anonymous:
            isfavorite = False
        else:
            isfavorite = get_isfavorite(user=user, tourid=tourid)

        return Response(
            {
                "isfavorite": isfavorite,
                # "hotel": hoteldetail.json()["data"]["hotel"],
                "tour": tour.json()["data"]["tour"],
                "flights": flights,
            }
        )


class RecommendationsView(APIView):
    def get(self, request):
        authlogin = settings.AUTHLOGIN
        authpass = settings.AUTHPASS

        recommendations = requests.get(
            f"http://tourvisor.ru/xml/hottours.php?picturetype=1&items=30"
            f"&format=json&authpass={authpass}&authlogin={authlogin}"
        )

        if recommendations.status_code != 200:
            return Response({"response": False})
        return Response(recommendations.json())
