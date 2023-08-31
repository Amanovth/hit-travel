from django.db import models
from django.utils.translation import gettext_lazy as _


class Departures(models.Model):
    sub_id = models.CharField(_('ID'), null=True, blank=True, max_length=10)
    name = models.CharField(_('Name'), max_length=50, null=True, blank=True)
    namefrom = models.CharField(_('Name from'), max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name


class Country(models.Model):
    sub_id = models.CharField(_('ID'), null=True, blank=True, max_length=10)
    name = models.CharField(_('Name'), max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'


class Tour(models.Model):
    title = models.CharField(_('Tour'), max_length=100, null=True, blank=True)
    departure = models.ForeignKey(Departures, on_delete=models.CASCADE, null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Tour')
        verbose_name_plural = _('Tours')
