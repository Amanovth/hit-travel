from django.urls import path
from .search_views import *
from .views import *

urlpatterns = [
    # Search tours
    path('search', SearchView.as_view(), name='search'),
    path('filter-params', FilterParams.as_view(), name='filter-options'),
    # Actualization
    path('actualize/<str:tourid>', TourActualizeView.as_view(), name='actualize'),
    path('detail/tour/<str:tourid>', TourActdetailView.as_view(), name='tour-detail'),
    # Hotel info
    path('detail/hotel/<str:hotelcode>', HotelDetailView.as_view(), name='hotel-detail'),
    # Add to favorites
    path('favorite/hotel/<int:hotelcode>', AddRemoveHotelFavoriteView.as_view(), name='add-to-favorite-hotel'),
    path('favorite/tour/<int:tourid>', AddRemoveTourFavoriteView.as_view(), name='add-to-favorite-tour'),
    path('favorite/list', FavoriteToursAPIView.as_view(), name='favorite-list')
]