from rest_framework.generics import ListAPIView, RetrieveAPIView

from .models import Stories, Versions
from .serializers import StoriesSerializers, VersionsSerializer


class StoriesView(ListAPIView):
    queryset = Stories.objects.all()
    serializer_class = StoriesSerializers


class VersionsView(RetrieveAPIView):
    serializer_class = VersionsSerializer

    def get_object(self):
        return Versions.objects.latest("date")