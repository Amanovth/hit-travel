from django.urls import path
from .views import *

urlpatterns = [
    path('api/search', SearchView.as_view(), name='search'),
    path('api/filter-options', FilterOptions.as_view(), name='filter-options')
]