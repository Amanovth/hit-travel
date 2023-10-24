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
        "number": f"{user.bcard_number}000",
        "user_id": int(user.tourist_id),
        # "manager_id": manager_id,
    }

    url_1 = f"https://api.u-on.ru/{KEY}/bcard/create.json"
    res_1 = requests.post(url_1, data=data_1)
    bcard_id = res_1.json()["id"]
    user.bcard_id = bcard_id
    user.save()

    # Activate
    data_2 = {"bc_number": f"{user.bcard_number}000", "user_id": int(user.tourist_id)}

    url_2 = f"https://api.u-on.ru/{KEY}/bcard-activate/create.json"
    res_2 = requests.post(url_2, data_2)
    return True


def create_lead(data, user):
    url = f"https://api.u-on.ru/{KEY}/lead/create.json"

    # Примечание
    note = (
        # f"{data['first_name']} {data['last_name']}, {data['gender']}\n"
        # f"Телефон: {data['phone']}\n"
        # f"Email: {data['email']}\n"
        f"ИНН: {data['inn']}\n"
        f"ID пасспорта: {data['passport_id']}\n"
        f"Страна: {data['country']}\n"
        f"Город: {data['city']}\n"
        f"Бонусы: {data['bonuses']}\n"
        f"Количество путешественников: {len(data['travelers'])}\n"
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
        "source": "Мобильное приложение",
        "extended_fields": [111046],
    }

    res = requests.post(url, data=r_data)

    if res.status_code != 200:
        return False
    return res.json()


def decrease_bonuses(bcard_id, bonuses, reason):
    url = f"https://api.u-on.ru/{KEY}/bcard-bonus/create.json"

    data = {
        "bc_id": bcard_id,
        "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "type": 2,
        "bonuses": bonuses,
        "reason": reason,
    }

    res = requests.post(url, data=data)
    
    if res.status_code != 200:
        return False
    return True