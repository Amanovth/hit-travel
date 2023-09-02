import requests
from rest_framework import views, permissions, status
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

from .models import Favorites
from .serializers import *


class AddRemoveTourFavoriteView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, tourid):
        user = request.user
        favorite, created = Favorites.objects.get_or_create(user=user, tourid=tourid)

        if not created:
            favorite.delete()
            return Response(
                {"response": True, "detail": "Removed from favorites"},
                status=status.HTTP_200_OK,
            )

        return Response(
            {"response": True, "detail": "Added to favorites"},
            status=status.HTTP_200_OK,
        )


class FavoriteToursListView(views.APIView):
    def get(self, request):
        authlogin = settings.AUTHLOGIN
        authpass = settings.AUTHPASS

        queryset = Favorites.objects.filter(user=request.user)
        serializer = FavoriteToursSerializer(queryset, many=True)
        reponse = []

        for i in serializer.data:
            detail = requests.get(
                f"http://tourvisor.ru/xml/actualize.php?tourid={i['tourid']}&request=0"
                f"&format=json&authpass={authpass}&authlogin={authlogin}"
            )
            detail.raise_for_status()
            flights = requests.get(
                f"http://tourvisor.ru/xml/actdetail.php?tourid={i['tourid']}"
                f"&format=json&authpass={authpass}&authlogin={authlogin}"
            )
            flights.raise_for_status()
            reponse.append({'detail': detail.json(), 'flights': flights.json()})
            
        return Response(reponse)
