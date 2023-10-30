from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from .models import BusTours, Reviews, Category
from .serializers import (
    BusTourListSerializer,
    BusTourDetailSerializer,
    ReviewCreateSerializer,
    CategorySerializer,
)
from .filters import BusToursFilter


class BusTourListAPIView(ListAPIView):
    queryset = BusTours.objects.all()
    serializer_class = BusTourListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = BusToursFilter


class BusTourListParamsAPIView(APIView):
    def get(self, request):
        datefrom_values = BusTours.objects.values_list("datefrom", flat=True).distinct()

        departure_choices = [
            {"name": choice[0]} for choice in BusTours.DEPARTURE_CHOICES
        ]
        
        categories = Category.objects.all()
        category_serializer = CategorySerializer(categories, many=True)

        return Response(
            {
                "datefrom": list(datefrom_values),
                "categories": category_serializer.data,
                "departures": departure_choices,
            }
        )


class BusTourDetailAPIView(RetrieveAPIView):
    queryset = BusTours.objects.all()
    serializer_class = BusTourDetailSerializer


class ReviewCreateAPIView(CreateAPIView):
    queryset = Reviews.objects.all()
    serializer_class = ReviewCreateSerializer