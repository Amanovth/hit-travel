from django.urls import path
from .views import (
    BusTourListAPIView, 
    BusTourDetailAPIView, 
    BusTourListParamsAPIView, 
    ReviewCreateAPIView, 
    BusTourRequestAPIView,
)


urlpatterns = [
    path("bus-tour/list", BusTourListAPIView.as_view(), name='bus-tour-list'),
    path("bus-tour/list-params", BusTourListParamsAPIView.as_view(), name='bus-tour-list-params'),
    path("bus-tour/detail/<int:pk>", BusTourDetailAPIView.as_view(), name="bus-tour-detail"),
    path("bus-tour/review-create", ReviewCreateAPIView.as_view(), name="review-create"),
    path("bus-tour/request", BusTourRequestAPIView.as_view(), name="bus-tour-request")
]