import os

import httpx
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .filters import Search
from asgiref.sync import async_to_sync


async def get_search_results(query_params):
    url = f'http://tourvisor.ru/xml/search.php?format=json'

    for param, value in query_params.items():
        url += f"&{param}={value}"

    async with httpx.AsyncClient() as client:
        res = await client.get(url)
        res.raise_for_status()
        return res.json()


def async_search_view(request):
    async def search_view_inner():
        if request.method == 'GET':
            authlogin = os.getenv('AUTHLOGIN')
            authpass = os.getenv('AUTHPASS')

            search_results = await get_search_results(request.query_params)
            requestid = search_results['result']['requestid']
            print(requestid)

            url = f'http://tourvisor.ru/xml/result.php?format=json&requestid={requestid}&authlogin={authlogin}&authpass={authpass}'

            async with httpx.AsyncClient() as client:
                res = await client.get(url)
                print(url)
                res.raise_for_status()

                return Response(res.json())

    return async_to_sync(search_view_inner)()


search_view = api_view(['GET'])(async_search_view)
