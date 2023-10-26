import requests
from django.conf import settings
from datetime import datetime, timedelta

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
        f"Страна: {data['country']}\n"
        f"Город: {data['city']}\n"
        f"Количество путешественников: {len(data['travelers'])}\n"
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
        "extended_fields": {
            "111046": data["operatorlink"],
            "111345": data["inn"],
            "111352": data["passport_id"],
            "111347": data["bonuses"],
        },
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


def increase_bonuses(bcard_id, bonuses, reason):
    url = f"https://api.u-on.ru/{KEY}/bcard-bonus/create.json"

    till_date = datetime.now() + timedelta(days=30)

    data = {
        "bc_id": bcard_id,
        "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "type": 1,
        "bonuses": bonuses,
        "reason": reason,
        "till_date": till_date.strftime("%Y-%m-%d %H:%M:%S"),
    }

    res = requests.post(url, data=data)

    if res.status_code != 200:
        return False
    return True
