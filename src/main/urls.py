from django.urls import path
from .views import StoriesView, VersionsView


urlpatterns = [
    path("stories", StoriesView.as_view(), name="stories"),
    path("versions", VersionsView.as_view(), name="versions")
]
