from rest_framework import serializers

from .models import *


class DepartureCreateAPIViewSerializers(serializers.ModelSerializer):
    class Meta:
        model = Departures
        fields = '__all__'


class CountryCreateAPIViewSerializers(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


from rest_framework import serializers


class SearchParamsSerializer(serializers.Serializer):
    authlogin = serializers.CharField()
    authpass = serializers.CharField()
    departure = serializers.IntegerField(required=False)
    country = serializers.IntegerField(required=False)
    datefrom = serializers.DateField(required=False)
    dateto = serializers.DateField(required=False)
    nightsfrom = serializers.IntegerField(default=7)
    nightsto = serializers.IntegerField(default=10)
    adults = serializers.IntegerField(default=2)
    child = serializers.IntegerField(default=0)
    childage1 = serializers.IntegerField(required=False)
    childage2 = serializers.IntegerField(required=False)
    childage3 = serializers.IntegerField(required=False)
    stars = serializers.IntegerField(required=False)
    starsbetter = serializers.IntegerField(default=1, required=False)
    meal = serializers.CharField(required=False)
    mealbetter = serializers.IntegerField(default=1, required=False)
    rating = serializers.IntegerField(required=False)
    hotels = serializers.CharField(required=False)
    hoteltypes = serializers.CharField(required=False)
    pricetype = serializers.IntegerField(default=0, required=False)
    regions = serializers.CharField(required=False)
    subregions = serializers.CharField(required=False)
    operators = serializers.CharField(required=False)
    pricefrom = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    priceto = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    currency = serializers.IntegerField(default=0)
    hideregular = serializers.IntegerField(default=0)
    services = serializers.CharField(required=False)
    format = serializers.ChoiceField(choices=['json', 'xml'], default='xml')
