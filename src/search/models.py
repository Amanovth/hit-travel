from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Favorites(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Пользователь'), on_delete=models.CASCADE, null=True, blank=True, related_name='user')
    tourid = models.CharField(_('Код тура'), max_length=100, null=True, blank=True)
    
    
    def __str__(self):
        return self.user.email
