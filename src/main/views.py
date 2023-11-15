import json
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Stories, Versions
from .serializers import StoriesSerializers, VersionsSerializer


class StoriesView(ListAPIView):
    queryset = Stories.objects.order_by("-id")
    serializer_class = StoriesSerializers


class VersionsView(RetrieveAPIView):
    serializer_class = VersionsSerializer

    def get_object(self):
        return Versions.objects.latest("date")
    

class CountriesJsonView(APIView):
    def get(self, request):
        with open("/home/chyngyz/hit-travel/src/main/countries.json", "r") as file:
            data = json.load(file)
        
        return Response(data)
