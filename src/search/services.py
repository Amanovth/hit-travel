from django.core.exceptions import ObjectDoesNotExist
from .models import Favorites
from src.account.models import TourRequest


def get_isfavorite(user, tourid):
    if user.is_anonymous:
        return False
    try:
        Favorites.objects.get(user=user, tourid=int(tourid))
        return True
    except ObjectDoesNotExist:
        return False


def get_isrequested(user, tourid):
    if user.is_anonymous:
        return False
    try:
        TourRequest.objects.get(user=user, tourid=int(tourid))
        return True
    except ObjectDoesNotExist:
        return False
