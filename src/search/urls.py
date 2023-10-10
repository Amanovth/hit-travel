from django.urls import path
from .search_views import *
from .views import *

urlpatterns = [
    # Search tours
    path('api/search', SearchView.as_view(), name='search'),
    path('api/filter-params', FilterParams.as_view(), name='filter-options'),
    path('api/country/<int:departureid>', FilterCountries.as_view(), name='get-countries'),
    path('api/hotels/<int:hotcountry>', FilterHotels.as_view(), name='get-hotels'),
    path('api/regions/<int:regcountry>', RegCountryView.as_view(), name='regcountry'),
    path('api/hottours', HotToursListView.as_view(), name='hottours'),
    path('api/recommendations', RecommendationsView.as_view(), name='recommendations '),
    # Actualization
    path('api/detail/tour/<str:tourid>', TourDetailView.as_view(), name='hottours'),
    # path('api/detail/tour/<str:tourid>', TourActualizeView.as_view(), name='actualize'),
    path('api/detail/flights/<str:tourid>', TourActdetailView.as_view(), name='tour-detail'),
    # Hotel info
    path('api/detail/hotel/<str:hotelcode>', HotelDetailView.as_view(), name='hotel-detail'),
    # Add to favorites
    path('favorite/tour/<int:tourid>', AddRemoveTourFavoriteView.as_view(), name='add-to-favorite-tour'),
    path('favorite/list', FavoriteToursListView.as_view(), name='favorite-list')
]