from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated

from .models import BusTours, Reviews, Category, BusTourRequest
from .serializers import (
    BusTourListSerializer,
    BusTourDetailSerializer,
    ReviewCreateSerializer,
    CategorySerializer,
    BusTourRequestSerializer,
)
from .filters import BusToursFilter
from .services import send_bustour_request


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


class BusTourRequestAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = BusTourRequest.objects.all()
    serializer_class = BusTourRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        user = request.user

        if serializer.is_valid():
            tour = serializer.validated_data.get("tour")
            existing_tour_request = BusTourRequest.objects.filter(
                tour=tour, user=user
            )

            if existing_tour_request.exists():
                return Response({"response": False})

            serializer.save(user=request.user)
            
            res = send_bustour_request(serializer.data, user)

            return Response(
                {
                    "response": True,
                    "message": "Заявка успешно отправлено",
                }
            )
        return Response(serializer.errors)
