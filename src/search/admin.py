from django.contrib import admin
from . models import Favorites


# @admin.register(Favorites)
# class FavoritesAdmin(admin.ModelAdmin):



admin.site.register(Favorites)