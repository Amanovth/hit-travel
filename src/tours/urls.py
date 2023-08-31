from django.urls import path
from .views import *
from .search_view import search_view

urlpatterns = [
    path('departure/create', DepartureCreateAPIView.as_view()),
    path('departure/list', DepartureListAPIView.as_view()),
    path('country/create', CountryCreateAPIView.as_view()),
    path('country/list', CountryListAPIView.as_view()),
    # path('search', search_view, name='search-view'),
    # path('', TestView.as_view(), name='search-view'),
]
