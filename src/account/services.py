import requests
from django.conf import settings
from datetime import datetime

KEY = settings.KEY


def get_user_by_phone(phone):
    url = f"https://api.u-on.ru/{KEY}/user/phone/{phone}.json"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()["users"][0]
    return False


def bonus_card_create(user):
    user_id = user.id

    # Create
    data_1 = {
        # "number": int(f"{user_id:<06d}"),
        "number": int(user_id),
        "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user_id": int(user.tourist_id),
        # "manager_id": manager_id,
    }

    url_1 = f"https://api.u-on.ru/{KEY}/bcard/create.json"
    res_1 = requests.post(url_1, data=data_1)

    # Activate
    data_2 = {"bc_number": int(user_id), "user_id": int(user.tourist_id)}

    url_2 = f"https://api.u-on.ru/{KEY}/bcard-activate/create.json"
    res_2 = requests.post(url_2, data_2)
    return True


def create_lead(data, user):
    url = f"https://api.u-on.ru/{KEY}/lead/create.json"

    # Примечание
    note = (
        f"{data['first_name']} {data['last_name']}\n"
        f"{data['phone']}\n"
        f"{data['email']}\n"
        f"Оператор: {data['operatorlink']}"
    )

    r_data = {
        "r_dat": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        # "r_u_id": user.manager_id,
        "r_cl_id": user.tourist_id,
        "u_surname": data["last_name"],
        "u_name": data["first_name"],
        "u_phone": data["phone"],
        "u_email": data["email"],
        "note": note,
    }

    res = requests.post(url, data=r_data)

    if res.status_code != 200:
        return False
    return True
