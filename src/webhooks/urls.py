from django.urls import path

from .views import (
    CreateRequestView,
    CreateClientView
)


urlpatterns = [
    path("create_request", CreateRequestView.as_view(), name="create_request"),
    path("create_client", CreateClientView.as_view(), name="create_client")
]
