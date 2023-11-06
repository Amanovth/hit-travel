from django.conf import settings
from datetime import datetime
import requests

KEY = settings.KEY


def create_service(data, user, request_number):
    url = f"https://api.u-on.ru/{KEY}/service/create.json"

    data = {
        "r_id": request_number,
        "type_id": 17,
        "description": f"Автобусный тур: {data['title']}",
        "date_begin": data["datefrom"],
        "date_end": data["dateto"],
        "country": data["country"],
        "nutrition": data["meal"],
        "duration": data["nights"],
        "tourists_count": len(data["bustour_travelers"]) + 1,
        "price": data["price"],
        "currency_id": 2,
        "currency_id_netto": 2
    }

    requests.post(url, data=data)

def send_bustour_request(data, user):
    url = f"https://api.u-on.ru/{KEY}/lead/create.json"

    # Примечание
    note = (
        f"Страна: {data['country']}\n"
        f"Город: {data['city']}\n"
    )

    r_data = {
        "r_dat": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "r_cl_id": user.tourist_id,
        "u_surname": data["last_name"],
        "u_name": data["first_name"],
        "u_phone": data["phone"],
        "u_email": data["email"],
        # "note": note,
        "source": "Мобильное приложение",
        "date_from": data["datefrom"],
        "date_to": data["dateto"],
        "nights_from": data["nights"],
        "nutrition": data["meal"],
        "tourist_count": data["num_of_tourists"],
        "budget": data["price"],
        "travel_type_id": 10,
    }

    res = requests.post(url, data=r_data)

    create_service(data, user, res.json()["id"])

    if res.status_code != 200:
        return False
    return res.json()
