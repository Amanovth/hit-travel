from django.contrib import admin

from .models import *

admin.site.register(Tour)
admin.site.register(Departures)


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('sub_id', 'name',)
    list_display_links = list_display
    ordering = ('name',)
