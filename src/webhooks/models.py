import requests
import time
import string
from random import choices
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from src.account.models import RequestTour, User, Traveler
from django.core.exceptions import ObjectDoesNotExist
from src.account.services import send_password_to_user


class CreateRequest(models.Model):
    uon_id = models.IntegerField(default=46194)
    uon_subdomain = models.CharField(max_length=255)
    datetime = models.DateTimeField()
    type_id = models.IntegerField()
    request_id = models.IntegerField()

    def __str__(self):
        return f"Обращения {self.request_id}"

    class Meta:
        verbose_name = _("Обращения CRM")
        verbose_name_plural = _("Обращения CRM")

    def save(self, *args, **kwargs):
        time.sleep(30)
        url = f"https://api.u-on.ru/{settings.KEY}/request/{self.request_id}.json"

        res = requests.get(url)

        if res.status_code != 200:
            return False

        data = res.json()["request"][0]

        if not data["client_id"]:
            res = requests.get(url)

            data = res.json()["request"][0]

        try:
            user = User.objects.get(tourist_id=data["client_id"])
        except ObjectDoesNotExist:
            user = None

        obj = RequestTour(
            user=user,
            status=1,
            first_name=data["client_name"],
            last_name=data["client_surname"],
            phone=data["client_phone"],
            email=data["client_email"],
            gender="",
            dateofborn="2022-12-12",
            inn=data["client_inn"],
            passport_id="",
            date_of_issue="2020-12-12",
            issued_by="1",
            validity="2020-12-12",
            instagram=data["instagram"],
            tourid="0",
            operatorlink="https://hit-travel.org",
            request_number=self.request_id
        )

        obj.save()

        if data["tourists"]:
            for i in data["tourists"]:
                tourist = Traveler(first_name=i["u_name"], last_name=i["u_surname"], main=obj)
                tourist.save()

        super(CreateRequest, self).save(*args, **kwargs)


class CreateClient(models.Model):
    uon_id = models.IntegerField(default=46194)
    uon_subdomain = models.CharField(max_length=255)
    datetime = models.DateTimeField()
    type_id = models.IntegerField()
    client_id = models.IntegerField()

    def __str__(self) -> str:
        return f"Клиент {self.client_id}"

    class Meta:
        verbose_name = _("Клиент CRM")
        verbose_name_plural = _("Клиенты CRM")

    def save(self, *args, **kwargs):
        # time.sleep(10)
        # url = f"https://api.u-on.ru/{settings.KEY}/user/{self.client_id}.json"
        
        # res = requests.get(url)

        # if res.status_code != 200:
        #     return
        
        # data = res.json()["user"][0]

        # if not data["u_id"]:
        #     res = requests.get(url)
        #     data = res.json()["user"][0]

        # obj = User(
        #     tourist_id=data["u_id"],
        #     first_name=data["u_surname"],
        #     last_name=data["u_name"],
        #     first_name_en=data["u_surname_en"],
        #     last_name_en=data["u_name_en"],
        #     email=data["u_email"],
        #     phone=data["u_phone"],
        #     inn=data["u_inn"],
        #     bcard_id=data["bcard_id"],
        #     bcard_number=data["bcard_number"],
        #     created=2,
        #     passport_id=data["u_zagran_number"],
        #     # date_of_issue=data["u_zagran_given"],
        #     # validity=data["u_zagran_expire"],
        #     issued_by=data["u_zagran_organization"]
        # )

        # new_password = "".join(
        #     choices(string.ascii_letters + string.digits, k=8)
        # )
        # obj.set_password(new_password)
        # obj.save()

        # send_password_to_user(self, new_password)

        return super().save(*args, **kwargs)
