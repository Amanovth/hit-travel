import requests
import pdfkit
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.template.loader import get_template
from django.core.files.base import ContentFile
from datetime import datetime, timedelta
from num2words import num2words
from src.base.utils import Util

KEY = settings.KEY
AUTHLOGIN = settings.AUTHLOGIN
AUTHPASS = settings.AUTHPASS


permissions = (
    _("Permissions"),
    {
        "fields": (
            "is_active",
            "is_staff",
            "is_superuser",
            "groups",
            "user_permissions",
        ),
    },
)


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


def create_dogovor(instance):
    date = datetime.now().strftime("%d.%m.%Y %H:%M")
    price_word = num2words(int(instance.price), lang="ru")
    surcharge_word = num2words(int(instance.surcharge), lang="ru")

    tour = requests.get(f"https://hit-travel.org/api/detail/tour/{instance.tourid}")

    context = {
        "obj": instance,
        "date": date,
        "price_word": price_word,
        "surcharge_word": surcharge_word,
        "operatorname": tour.json()["tour"]["operatorname"],
        "flydate": tour.json()["tour"]["flydate"],
        "nights": tour.json()["tour"]["nights"],
    }

    template = get_template("index.html")
    html = template.render(context)

    pdf = pdfkit.from_string(html, False)

    instance.agreement.save(
        f"agreement_pdf_{instance.request_number}.pdf",
        ContentFile(pdf),
        save=True,
    )


def create_service(request_number, data=None, instance=None):
    url = f"https://api.u-on.ru/{KEY}/service/create.json"

    if data:
        tour = requests.get(
            f"http://tourvisor.ru/xml/actualize.php?authlogin={AUTHLOGIN}&authpass={AUTHPASS}&format=json&tourid={data['tourid']}"
        )
    if instance:
        tour = requests.get(
            f"http://tourvisor.ru/xml/actualize.php?authlogin={AUTHLOGIN}&authpass={AUTHPASS}&format=json&tourid={instance.tourid}"
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
        "source": "Мобильное приложение",
    }

    res = requests.post(url, data=r_data)

    create_service(res.json()["id"], data=data)

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

    till_date = datetime.now() + timedelta(days=365)

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

    if instance.user:
            user = instance.user
            instance.email = user.email
            instance.phone = user.phone
            instance.first_name = user.first_name
            instance.last_name = user.last_name
            instance.gender = user.gender
            instance.dateofborn = user.dateofborn
            instance.inn = user.inn
            instance.passport_id = user.passport_id
            instance.date_of_issue = user.date_of_issue
            instance.issued_by = user.issued_by
            instance.validity = user.validity
            instance.city = user.city
            instance.country = user.county
            instance.passport_front = user.passport_front
            instance.passport_back = user.passport_back
            instance.save()

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
        "source": "Мобильное приложение",
    }

    res = requests.post(url, data)

    instance.request_number = res.json()["id"]
    instance.save()

    if instance.tourid:
        create_service(res.json()["id"], instance=instance)
        create_dogovor(instance)


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

    if instance.groups:
        return

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


def create_managers():
    url = "https://api.u-on.ru/RxH3WeM378er81w4dMuF1649063416/manager.json"

    # response =
