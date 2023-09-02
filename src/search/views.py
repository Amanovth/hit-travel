from rest_framework import views, permissions, status
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from .models import Favorites
from django.conf import settings



class AddRemoveHotelFavoriteView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, hotelcode):
        user = request.user
        favorite, created = Favorites.objects.get_or_create(user=user, hotelcode=hotelcode)

        if not created:
            favorite.delete()
            return Response({"response": True, "detail": "Removed from favorites"}, status=status.HTTP_200_OK)

        return Response({"response": True, "detail": "Added to favorites"}, status=status.HTTP_200_OK)


class AddRemoveTourFavoriteView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, tourid):
        user = request.user
        favorite, created = Favorites.objects.get_or_create(user=user, tourid=tourid)

        if not created:
            favorite.delete()
            return Response({"response": True, "detail": "Removed from favorites"}, status=status.HTTP_200_OK)

        return Response({"response": True, "detail": "Added to favorites"}, status=status.HTTP_200_OK)


class FavoriteToursAPIView(views.APIView):
    def get_queryset(self):
        return Favorites.objects.filter(user=self.request.user)
