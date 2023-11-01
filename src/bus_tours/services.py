from django.conf import settings
from datetime import datetime
import requests

KEY = settings.KEY


def send_bustour_request(data, user):
    url = f"https://api.u-on.ru/{KEY}/lead/create.json"

    # Примечание
    note = (
        f"Страна: {data['country']}\n"
        f"Город: {data['city']}\n"
        f"Количество путешественников: {len(data['bustour_travelers'])}\n"
    )

    r_data = {
        "r_dat": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "r_cl_id": user.tourist_id,
        "u_surname": data["last_name"],
        "u_name": data["first_name"],
        "u_phone": data["phone"],
        "u_email": data["email"],
        "note": note,
        "source": "Автобусный тур",
        "date_from": data["datefrom"],
        "date_to": data["dateto"],
        "nights_from": data["nights"],
        "nutrition": data["meal"],
        "tourist_count": data["num_of_tourists"],
        "budget": data["price"],
        "extended_fields": {
            "111345": data["inn"],
            "111352": data["passport_id"],
        },
    }

    res = requests.post(url, data=r_data)

    if res.status_code != 200:
        return False
    return res.json()
