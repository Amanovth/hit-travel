import time
import httpx
import requests
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings


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
        requestid = self.get_search_result(request.query_params)

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
            f"http://tourvisor.ru/xml/listdev.php?type="
            f"country,departure,region,subregion,meal,stars,operator,currency,services"
            f"&format=json&authpass={authpass}&authlogin={authlogin}"
        )

        if options.status_code != 200:
            return Response({"response": False})
        return Response(options.json())


class FilterCountries(APIView):
    def get(self, request, departureid):
        authlogin = settings.AUTHLOGIN
        authpass = settings.AUTHPASS

        countries = requests.get(
            f"http://tourvisor.ru/xml/listdev.php?type=country&cndep={departureid}"
            f"&format=json&authpass={authpass}&authlogin={authlogin}"
        )
        if countries.status_code != 200:
            return Response({"response": False})
        return Response(countries.json())


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
        return Response(actualize.json())


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
        return Response(hoteldetail.json())


class HotToursView(APIView):
    def get(self, request):
        authlogin = settings.AUTHLOGIN
        authpass = settings.AUTHPASS

        hottours = requests.get(
            f"http://tourvisor.ru/xml/hottours.php?city=80&picturetype=1"
            f"&format=json&authpass={authpass}&authlogin={authlogin}&reviews=1"
        )

        if hottours.status_code != 200:
            return Response({"response": False})
        return Response(hottours.json())


class HotTourDetailView(APIView):
    def get(self, request, tourid):
        authlogin = settings.AUTHLOGIN
        authpass = settings.AUTHPASS

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

        try:
            hoteldetail = requests.get(
                f"http://tourvisor.ru/xml/hotel.php?hotelcode={tour.json()['data']['tour']['hotelcode']}"
                f"&format=json&authpass={authpass}&authlogin={authlogin}&reviews=1"
            )

            if hoteldetail.status_code != 200:
                return Response({"response": False})
        except KeyError:
            return Response({"reponse": False})

        # Get flights on this tour
        try:
            flights = requests.get(
                f"http://tourvisor.ru/xml/actdetail.php?tourid={tourid}"
                f"&format=json&authpass={authpass}&authlogin={authlogin}"
            )
            if flights.status_code != 200:
                return Response({"response": False})
        except KeyError:
            return Response({"response": False})

        return Response(
            {
                "hotel": hoteldetail.json()["data"]["hotel"],
                "tour": tour.json()["data"]["tour"],
                "flights": flights.json(),
            }
        )
