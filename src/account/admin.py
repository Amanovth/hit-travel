from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin, Group
from .models import *


class OrderHistoryInline(admin.StackedInline):
    model = OrderHistory
    extra = 0


class BonusHistory(admin.StackedInline):
    model = BonusHistory
    extra = 0


@admin.register(User)
class UserAdmin(UserAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "password",
                    "tourist_id",
                    "manager_id",
                    "balance",
                    "bonuses",
                )
            },
        ),
        (
            _("Personal info"),
            {
                "fields": (
                    "phone",
                    "first_name",
                    "last_name",
                    "photo",
                    "county",
                    "passport_id",
                    "date_birth",
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
        (
            _("Верификация"),
            {"fields": ("is_verified", "verification_code", "verification_code_time")},
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "phone",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                ),
            },
        ),
    )

    list_display = ("id", "email", "first_name", "last_name", "is_staff")
    list_display_links = ("id", "email")
    search_fields = ("first_name", "last_name", "email")
    ordering = ("email",)
    inlines = (
        OrderHistoryInline,
        BonusHistory,
    )


@admin.register(TourRequest)
class TourRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "phone", "first_name", "last_name")
    list_display_links = ("id", "user")
    search_fields = ("email", "phone", "first_name", "last_name", "inn")
