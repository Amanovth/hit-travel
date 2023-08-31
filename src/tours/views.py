import requests
from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend

from .models import *
from .serializers import *
from rest_framework.pagination import PageNumberPagination
from .filters import Search


class DepartureCreateAPIView(generics.CreateAPIView):
    queryset = Departures.objects.all()
    serializer_class = DepartureCreateAPIViewSerializers


class DepartureListAPIView(generics.ListAPIView):
    queryset = Departures.objects.all()
    serializer_class = DepartureCreateAPIViewSerializers
    pagination_class = PageNumberPagination


class CountryCreateAPIView(generics.CreateAPIView):
    queryset = Country.objects.all()
    serializer_class = CountryCreateAPIViewSerializers

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            sub_id = serializer.data['sub_id']

            country, created = self.queryset.get_or_create(sub_id=sub_id, defaults={'name': serializer.data['name']})

            if created:
                return Response({'response': True}, status=status.HTTP_201_CREATED)
            else:
                return Response({'response': False}, status=status.HTTP_200_OK)


class CountryListAPIView(generics.ListAPIView):
    queryset = Country.objects.all()
    serializer_class = CountryCreateAPIViewSerializers
    pagination_class = PageNumberPagination


class TestView(APIView):
    def get(self, request):
        res = requests.get(
            'http://tourvisor.ru/xml/result.php?format=json&requestid=6138122095&authlogin=info@hit-travel.kg&authpass=qbJbXlT1pBrL'
        )

        return Response(res.json())
