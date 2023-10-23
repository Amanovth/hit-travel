from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin, Group
from ckeditor.widgets import CKEditorWidget
from .models import *


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
                    # "bcard_number",
                    "bcard_id",
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
    ordering = ("id",)
    inlines = (BonusHistory,)


class TravelersInline(admin.StackedInline):
    model = Travelers
    extra = 0


@admin.register(TourRequest)
class TourRequestAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "request_number",
        "status",
        "phone",
        "first_name",
        "last_name",
        "tourid",
        "created_at",
    )
    list_editable = ("status",)
    list_filter = ("status",)
    list_display_links = ("id", "user")
    search_fields = ("email", "phone", "first_name", "last_name", "inn")
    inlines = (TravelersInline,)

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "request_number",
                    "user",
                    "first_name",
                    "last_name",
                    "phone",
                    "email",
                    "gender",
                    "citizenship",
                    "inn",
                    "city",
                    "country",
                    "passport_id",
                    "bonuses",
                )
            },
        ),
        (
            _("Информация о туре"),
            {"fields": ("operatorlink", "tourid", "price", "currency")},
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


@admin.register(Payments)
class PaymentsAdmin(admin.ModelAdmin):
    model = Payments
    list_display = ("id", "bank_name")
    list_display_links = list_display
    formfield_overrides = {models.TextField: {"widget": CKEditorWidget()}}
    

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("id", "question",)
    list_display_links = list_display
