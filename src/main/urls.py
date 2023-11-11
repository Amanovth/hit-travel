from django.urls import path
from .views import StoriesView, VersionsView, CountriesJsonView


urlpatterns = [
    path("stories", StoriesView.as_view(), name="stories"),
    path("versions", VersionsView.as_view(), name="versions"),
    path("countries", CountriesJsonView.as_view(), name="countries")
]
