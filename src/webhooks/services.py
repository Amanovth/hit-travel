import requests
from django.conf import settings
from src.account.models import RequestTour
from src.account.models import User
from django.core.exceptions import ObjectDoesNotExist

KEY = settings.KEY


def get_client(tourist_id):
    pass


def add_request(sender, instance):
    url = f"https://api.u-on.ru/{KEY}/lead/{instance.request_id}.json"

    res = requests.get(url)

    if res.status_code != 200:
        return False

    data = res.json()["lead"][0]

    obj = RequestTour(
        first_name=data["client_name"],
        last_name=data["client_surname"],
        phone=data["client_phone"],
        email=data["client_phone"],
    )

    obj.save()


def add_client(sender, instance):
    url = f"https://api.u-on.ru/RxH3WeM378er81w4dMuF1649063416/user/{instance.request_id}.json"