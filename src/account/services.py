import requests
import string
from random import choices
from django.conf import settings
from datetime import datetime, timedelta
from src.base.utils import Util

KEY = settings.KEY
AUTHLOGIN = settings.AUTHLOGIN
AUTHPASS = settings.AUTHPASS


def update_user(data, user):
    url = f"https://api.u-on.ru/{KEY}/user/update/{user.tourist_id}.json"

    if data["gender"] == "Муж":
        u_sex = "m"
    else:
        u_sex = "f"

    r_data = {
        "u_birthday": data["dateofborn"],
        "u_zagran_given": data["date_of_issue"],
        "u_zagran_expire": data["validity"],
        "u_zagran_organization": data["issued_by"],
        "u_zagran_number": data["passport_id"],
        "u_sex": u_sex,
        "u_inn": data["inn"],
    }

    user.dateofborn = data["dateofborn"]
    user.date_of_issue = data["date_of_issue"]
    user.validity = data["validity"]
    user.issued_by = data["issued_by"]
    user.passport_id = data["passport_id"]
    user.inn = data["inn"]
    user.save()

    requests.post(url, r_data)


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


def create_service(data, user, request_number):
    url = f"https://api.u-on.ru/{KEY}/service/create.json"

    tour = requests.get(
        f"http://tourvisor.ru/xml/actualize.php?authlogin={AUTHLOGIN}&authpass={AUTHPASS}&format=json&tourid={data['tourid']}"
    )

    tour_data = tour.json()["data"]["tour"]

    data = {
        "r_id": request_number,
        "type_id": 12,
        "description": f"Тур: {tour_data['tourname']}\nГород вылета: {tour_data['departurename']}\nОператор: {tour_data['operatorname']}",
        "date_begin": tour_data["flydate"],
        # "date_end": data["dateto"],
        "country": tour_data["countryname"],
        "city": tour_data["hotelregionname"],
        "country": tour_data["countryname"],
        "nutrition": tour_data["meal"],
        "duration": tour_data["nights"],
        "tourists_count": tour_data["adults"],
        "tourists_child_count": tour_data["child"],
        "hotel": tour_data["hotelname"],
        "hotel_type": tour_data["room"],
        "price": tour_data["price"],
        "currency_id": 2,
        "currency_id_netto": 2,
        # "supplier_id": int(tour_data["operatorcode"]),
    }

    requests.post(url, data=data)


def create_lead(data, user):
    update_user(data, user)

    url = f"https://api.u-on.ru/{KEY}/lead/create.json"

    # Примечание
    note = f"Оператор: {data['operatorlink']}\n"

    r_data = {
        "r_dat": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "r_cl_id": user.tourist_id,
        "u_surname": data["last_name"],
        "u_name": data["first_name"],
        "u_phone": data["phone"],
        "u_email": data["email"],
        "note": note,
        "source": "Мобильное приложение"
    }

    res = requests.post(url, data=r_data)

    create_service(data, user, res.json()["id"])

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


def add_lead_on_creation(sender, instance):
    url = f"https://api.u-on.ru/{KEY}/lead/create.json"

    # Примечание
    note = f"Оператор: {instance.operatorlink}\n"

    data = {
        "r_dat": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "r_cl_id": instance.user.tourist_id,
        "u_surname": instance.last_name,
        "u_name": instance.first_name,
        "u_phone": instance.phone,
        "u_email": instance.email,
        "note": note,
        "source": "Мобильное приложение"
    }

    res = requests.post(url, data)


def send_password_to_user(instance, password):
    email_body = (
        f"Привет! {instance.last_name} {instance.first_name}\n\n"
        f"Чтобы войти в нашу систему, используйте этот адрес электронной почты и пароль:\n\n"
        f"{instance.email}\n"
        f"{password}"
    )

    email_data = {
        "email_body": email_body,
        "email_subject": "Подтвердите регистрацию",
        "to_email": instance.email,
    }

    Util.send_email(email_data)


def add_tourist_on_user_creation(sender, instance):
    url = f"https://api.u-on.ru/{KEY}/user/create.json"

    data = {
        "u_surname": instance.last_name,
        "u_name": instance.first_name,
        "u_sname": instance.surname,
        "u_email": instance.email,
        "u_phone_mobile": instance.phone,
        "u_birthday": instance.dateofborn,
        "u_inn": instance.inn,
        "u_zagran_number": instance.inn,
        "u_zagran_given": instance.date_of_issue,
        "u_zagran_expire": instance.validity,
        "u_zagran_organization": instance.issued_by,
        "u_birthday_place": f"{instance.city} {instance.county}",
        "u_password": instance.password_readable,
        "u_sex": instance.gender,
        "u_social_vk": instance.u_social_vk,
        "u_social_fb": instance.u_social_fb,
        "u_social_ok": instance.u_social_ok,
        "u_telegram": instance.u_telegram,
        "u_whatsapp": instance.u_whatsapp,
        "u_viber": instance.u_viber,
        "u_instagram": instance.u_instagram,
    }

    res = requests.post(url, data)

    if res.status_code != 200:
        return False
    
    instance.tourist_id = res.json()["id"]
    instance.is_verified = True
    instance.save()

    send_password_to_user(instance, instance.password_readable)

    bonus_card_create(instance)

    return
