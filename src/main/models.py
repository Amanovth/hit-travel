from django.db import models
from django.utils.translation import gettext_lazy as _


class Stories(models.Model):
    created_at = models.DateTimeField(_("Дата и время"), auto_now_add=True)
    img = models.ImageField(_("Изображение"), upload_to="story_images", null=True, blank=True)

    class Meta:
        verbose_name = _("История")
        verbose_name_plural = _("Истории")


class StoryVideos(models.Model):
    story = models.ForeignKey(Stories, on_delete=models.CASCADE, related_name="stories")
    url = models.FileField(_("История"), upload_to="stories")
    views = models.IntegerField(_("Количество просмотров"), default=1)
    created_at = models.DateTimeField(_("Дата и время"), auto_now_add=True)

    class Meta:
        verbose_name = _("История")
        verbose_name_plural = _("Истории")

    def __str__(self) -> str:
        return self.created_at.strftime("%d %B %Y г. %H:%M")


class Versions(models.Model):
    version = models.CharField(_("Версия"), max_length=255)
    appstore = models.URLField(_("App Store"), default="https://apps.apple.com/kg/app/hit-travel/id6467560261")
    googleplay = models.URLField(_("Google Play"), default="https://play.google.com/store/apps/details?id=com.hit.travel")
    date = models.DateTimeField(_("Дата"), auto_now_add=True)
    
    class Meta:
        verbose_name = _("Версия приложения")
        verbose_name_plural = _("Версии приложения")
        
    def __str__(self) -> str:
        return self.version

    
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