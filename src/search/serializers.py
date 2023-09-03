from rest_framework import serializers
from .models import Favorites


class FavoriteToursSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorites
        fields = '__all__'
