from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Favorites(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Пользователь"),
        on_delete=models.CASCADE,
        related_name="user",
    )
    date = models.DateTimeField(_("Дата"), auto_now_add=True)
    tourid = models.CharField(_("Код тура"), max_length=100, null=True, blank=True)

    def __str__(self):
        return self.user.email


class Currency(models.Model):
    CURRENCY_CHOICES = (
        ("USD", "USD"),
        ("EUR", "EUR")
    )

    currency = models.CharField(_("Валюта"), max_length=20, choices=CURRENCY_CHOICES, unique=True)
    purchase = models.DecimalField(_("Покупка"), max_digits=10, decimal_places=2)
    sell = models.DecimalField(_("Продажа"), max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return self.currency

    class Meta:
        verbose_name = _("Курс")
        verbose_name_plural = _("Курсы")
