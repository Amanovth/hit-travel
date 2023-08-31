import time
import httpx
import requests
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings


# class SearchView(APIView):
#     authlogin = settings.AUTHLOGIN
#     authpass = settings.AUTHPASS
#
#     def get_search_result(self, query_params):
#         search_url = (f'http://tourvisor.ru/xml/search.php?format=json'
#                       f'&authlogin={self.authlogin}&authpass={self.authpass}')
#
#         for param, value in query_params.items():
#             search_url += f'&{param}={value}'
#
#         requestid = requests.get(search_url)
#         requestid.raise_for_status()
#
#         return requestid.json()['result']['requestid']
#
#     def get(self, request):
#
#         requestid = self.get_search_result(request.query_params)
#
#         time.sleep(0.2)
#         url = (f'http://tourvisor.ru/xml/result.php?format=json&requestid={requestid}'
#                f'&authlogin={self.authlogin}&authpass={self.authpass}&onpage=1')
#
#         response = requests.get(url)
#         response.raise_for_status()
#
#         state = response.json()['data']['status']['state']
#
#         if state == 'finished':
#             return Response(response.json())
#         elif state == 'searching':
#             time.sleep(0.2)
#             return Response(response.json())
#         return Response('Time Out')


class SearchView(APIView):
    authlogin = settings.AUTHLOGIN
    authpass = settings.AUTHPASS

    def get_search_result(self, query_params):
        search_url = (f'http://tourvisor.ru/xml/search.php?format=json'
                      f'&authlogin={self.authlogin}&authpass={self.authpass}')

        for param, value in query_params:
            search_url += f'&{param}={value}'

        requestid = requests.get(search_url)
        requestid.raise_for_status()

        return requestid.json()['result']['requestid']

    def get_search_status(self, requestid):
        status_url = (f'http://tourvisor.ru/xml/result.php?format=json&requestid={requestid}'
                      f'&authlogin={self.authlogin}&authpass={self.authpass}&onpage=2')

        response = requests.get(status_url)
        response.raise_for_status()

        state = response.json()['data']['status']['state']
        return state, response.json()

    def get(self, request):

        requestid = self.get_search_result(request.query_params)
        state = 'searching'

        while state == 'searching':
            time.sleep(.1)
            state, response_data = self.get_search_status(requestid)

        if state == 'finished':
            return Response(response_data)
        else:
            return Response('Time Out')


class FilterOptions(APIView):
    def get(self, request):
        authlogin = settings.AUTHLOGIN
        authpass = settings.AUTHPASS

        options = requests.get(
            f'http://tourvisor.ru/xml/list.php?type='
            f'country,departure,region,subregion,meal,stars,operator,currency,services'
            f'&format=json&authpass={authpass}&authlogin={authlogin}'
        )
        options.raise_for_status()
        return Response(options.json())
