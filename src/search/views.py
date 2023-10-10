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
                {"response": True, "message": "Удалено из избранного"},
                status=status.HTTP_200_OK,
            )

        return Response(
            {"response": True, "message": "Добавлено в избранное"},
            status=status.HTTP_200_OK,
        )


class FavoriteToursListView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        authlogin = settings.AUTHLOGIN
        authpass = settings.AUTHPASS

        queryset = Favorites.objects.filter(user=request.user)
        serializer = FavoriteToursSerializer(queryset, many=True)
        response = []

        for i in serializer.data:
            detail = requests.get(
                f"http://tourvisor.ru/xml/actualize.php?tourid={i['tourid']}"
                f"&format=json&authpass={authpass}&authlogin={authlogin}"
            )

            flights = requests.get(
                f"http://tourvisor.ru/xml/actdetail.php?tourid={i['tourid']}"
                f"&format=json&authpass={authpass}&authlogin={authlogin}"
            )
            
            d = {}
            try:
                d['tourid'] = i['tourid']
                d['isfavorite'] = True
                d['tour'] = detail.json()['data']['tour']
            except KeyError:
                pass
            
            try: 
                d['flights'] = flights.json()['flights']
            except KeyError:
                d['flights'] = flights.json()
            
            response.append(d)
                
        return Response(response)
