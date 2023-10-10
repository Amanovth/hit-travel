from django.contrib import admin
from .models import Currency, Favorites
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import TokenProxy

@admin.register(Favorites)
class FavoritesAdmin(admin.ModelAdmin):
    list_display = ('user', 'tourid')


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ("id", "currency", "purchase", "sell",)
    list_display_links = ("id", "currency",)


admin.site.unregister(Group)
# admin.site.unregister(TokenProxy)
