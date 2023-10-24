from django.urls import path
from .views import StoriesView


urlpatterns = [
    path("stories", StoriesView.as_view(), name="stories")
]
