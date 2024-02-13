from django.contrib import admin
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import TokenProxy
from admin_extra_buttons.api import ExtraButtonsMixin, button, confirm_action, link, view
from admin_extra_buttons.utils import HttpResponseRedirect, HttpResponseRedirectToReferrer
from django.conf import settings
from .models import *
import requests
from django.utils.html import format_html

admin.site.unregister(Group)
admin.site.unregister(TokenProxy)

@admin.register(Countries)
class CountriesAdmin(ExtraButtonsMixin, admin.ModelAdmin):
    list_display = ['id', 'name', 'get_img']
    list_display_links = ['id', 'name', 'get_img']

    def get_img(self, obj):
        if obj.img:
            return format_html(f"<img src='{obj.img.url}' height='60'>")
        
    get_img.short_description = 'Изображение'


    @button(change_form=True, html_attrs={'style': 'background-color:#da2222; color:white; padding: 0.563rem 2.75rem; border-radius: 0.25rem;'})
    def Update(self, request):
        authlogin = settings.AUTHLOGIN
        authpass = settings.AUTHPASS
        countries = requests.get(
            f"http://tourvisor.ru/xml/list.php?type=country"
            f"&format=json&authpass={authpass}&authlogin={authlogin}"
        )
        countries = countries.json()
        
        for i in countries["lists"]["countries"]["country"]:
            try:
                obj = Countries.objects.get(name=i["name"])
            except:
                obj = Countries.objects.create(name=i["name"])
                obj.save()
    
        self.message_user(request, 'Список стран обновлен!')
        return HttpResponseRedirectToReferrer(request)