import requests
from django.conf import settings

KEY = settings.KEY

def get_user_by_phone(phone):
    url = f"https://api.u-on.ru/{KEY}/user/phone/{phone}.json"
    response = requests.get(url)
    return response.json()