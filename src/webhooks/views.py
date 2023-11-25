from rest_framework.generics import CreateAPIView

from .models import (
    CreateRequest,
    CreateClient,
)
from .serializers import (
    CreateRequestSerializer,
    CreateClientSerializer,
)


class CreateRequestView(CreateAPIView):
    queryset = CreateRequest.objects.all()
    serializer_class = CreateRequestSerializer


class CreateClientView(CreateAPIView):
    queryset = CreateClient.objects.all()
    serializer_class = CreateClientSerializer
