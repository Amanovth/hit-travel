import requests
import time
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver
from django.db.models.signals import post_save
from .services import add_request, add_client
from django.conf import settings
from src.account.models import RequestTour, User
from django.core.exceptions import ObjectDoesNotExist


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
        url = f"https://api.u-on.ru/{settings.KEY}/lead/{self.request_id}.json"

        res = requests.get(url)

        if res.status_code != 200:
            return False

        data = res.json()["lead"][0]

        if not data["client_id"]:
            res = requests.get(f"https://api.u-on.ru/{settings.KEY}/lead/{self.request_id}.json")

            data = res.json()["lead"][0]

        try:
            user = User.objects.get(tourist_id=data["client_id"])
        except ObjectDoesNotExist:
            user = None

        if user:
            issued_by = user.issued_by
        else:
            issued_by = ""

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
            issued_by=issued_by,
            validity="2020-12-12",
            instagram=data["instagram"],
            tourid="0",
            operatorlink="https://hit-travel.org",
            request_number=self.request_id
        )

        obj.save()

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
        return super().save(*args, **kwargs)


# @receiver(post_save, sender=CreateRequest)
# def add_request(sender, instance, created, **kwargs):
#     time.sleep(10)
#     url = f"https://api.u-on.ru/{settings.KEY}/lead/{instance.request_id}.json"

#     res = requests.get(url)

#     if res.status_code != 200:
#         return False

#     data = res.json()["lead"][0]

#     # user = User.objects.get(tourist_id=data["client_id"] + 1)

#     print(data["client_id"])

#     obj = RequestTour(
#         user_id=222,
#         first_name=data["client_name"],
#         last_name=data["client_surname"],
#         phone=data["client_phone"],
#         email=data["client_email"],
#         gender="Муж",
#         dateofborn="",
#         inn=data["client_inn"],
#         passport_id="user.passport_id",
#         date_of_issue="",
#         issued_by="user.issued_by",
#         validity="",
#         instagram=data["instagram"],
#         tourid="0",
#         operatorlink="https://hit-travel.org"
#     )

#     obj.save()


# @receiver(post_save, sender=CreateClient)
# def add_client(sender, instance, created, **kwargs):
#     if created:
#         add_client(sender, instance, created)
