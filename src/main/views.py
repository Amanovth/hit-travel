from rest_framework import generics

from .models import Stories
from .serializers import StoriesSerializers


class StoriesView(generics.ListAPIView):
    queryset = Stories.objects.all()
    serializer_class = StoriesSerializers
