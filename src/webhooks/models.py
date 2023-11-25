from django.db import models
from django.utils.translation import gettext_lazy as _


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
