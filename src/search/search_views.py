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
        requestid.raise_for_status()

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
        response.raise_for_status()

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
        options.raise_for_status()
        return Response(options.json())


class FilterCountries(APIView):
    def get(self, request, departureid):
        authlogin = settings.AUTHLOGIN
        authpass = settings.AUTHPASS

        countries = requests.get(
            f"http://tourvisor.ru/xml/listdev.php?type=country&cndep={departureid}"
            f"&format=json&authpass={authpass}&authlogin={authlogin}"
        )
        countries.raise_for_status()
        return Response(countries.json())


class TourActualizeView(APIView):
    def get(self, request, tourid):
        authlogin = settings.AUTHLOGIN
        authpass = settings.AUTHPASS

        actualize = requests.get(
            f"http://tourvisor.ru/xml/actualize.php?tourid={tourid}&request=0"
            f"&format=json&authpass={authpass}&authlogin={authlogin}"
        )
        actualize.raise_for_status()
        return Response(actualize.json())


class TourActdetailView(APIView):
    def get(self, request, tourid):
        authlogin = settings.AUTHLOGIN
        authpass = settings.AUTHPASS

        actualize = requests.get(
            f"http://tourvisor.ru/xml/actdetail.php?tourid={tourid}"
            f"&format=json&authpass={authpass}&authlogin={authlogin}"
        )
        actualize.raise_for_status()
        return Response(actualize.json())


class HotelDetailView(APIView):
    def get(self, request, hotelcode):
        authlogin = settings.AUTHLOGIN
        authpass = settings.AUTHPASS

        hoteldetail = requests.get(
            f"http://tourvisor.ru/xml/hotel.php?hotelcode={hotelcode}"
            f"&format=json&authpass={authpass}&authlogin={authlogin}&reviews=1"
        )

        hoteldetail.raise_for_status()
        return Response(hoteldetail.json())


# class SearchView(APIView):
#     authlogin = settings.AUTHLOGIN
#     authpass = settings.AUTHPASS

#     def get_search_result(self, query_params):
#         search_url = (
#             f"http://tourvisor.ru/xml/search.php?format=json"
#             f"&authlogin={self.authlogin}&authpass={self.authpass}"
#         )

#         for param, value in query_params.items():
#             search_url += f"&{param}={value}"

#         requestid = requests.get(search_url)
#         requestid.raise_for_status()

#         return requestid.json()["result"]["requestid"]

#     def get_search_status(self, requestid):
#         status_url = (
#             f"http://tourvisor.ru/xml/result.php?format=json&requestid={requestid}"
#             f"&authlogin={self.authlogin}&authpass={self.authpass}&onpage=2"
#         )

#         response = requests.get(status_url)
#         response.raise_for_status()

#         state = response.json()["data"]["status"]["state"]
#         return state, response.json()

#     def get(self, request):
#         requestid = self.get_search_result(request.query_params)
#         state = "searching"

#         while state == "searching":
#             time.sleep(0.1)
#             state, response_data = self.get_search_status(requestid)

#         if state == "finished":
#             return Response(response_data)
#         else:
#             return Response("Time Out")
