from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin
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
                    "first_name_en",
                    "last_name_en",
                    "dateofborn",
                    "photo",
                    "county",
                    "passport_id",
                    "inn",
                    "date_of_issue",
                    "issued_by",
                    "validity",
                    "city",
                    "passport_front",
                    "passport_back",
                )
            },
        ),
        (
            _("Социальные сети"),
            {
                "fields": (
                    "u_social_vk",
                    "u_social_fb",
                    "u_social_ok",
                    "u_telegram",
                    "u_whatsapp",
                    "u_viber",
                    "u_instagram"
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
                    "surname",
                    "dateofborn",
                    "inn",
                    "passport_id",
                    "city",
                    "county",
                    "date_of_issue",
                    "validity",
                    "issued_by",
                    "u_social_vk",
                    "u_social_fb",
                    "u_social_ok",
                    "u_telegram",
                    "u_whatsapp",
                    "u_viber",
                    "u_instagram",
                    "password1",
                    "password2",
                ),
            },
        ),
    )

    list_display = ("id", "email", "first_name", "last_name", "is_staff")
    list_display_links = ("id", "email")
    search_fields = (
        "first_name",
        "last_name",
        "email",
        "phone",
        "passport_id",
        "bcard_number",
    )
    ordering = ("-id",)


class TravelersInline(admin.StackedInline):
    model = Traveler
    extra = 0
    fields = ["first_name", "last_name"]


class DocumentsInline(admin.StackedInline):
    model = Document
    extra = 0


@admin.register(RequestTour)
class TourRequestAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "first_name",
        "last_name",
        "request_number",
        "status",
        "phone",
        "created_at",
        "user"
    )
    list_editable = ("status",)
    list_filter = ("status",)
    list_display_links = ("id", "first_name", "last_name", "request_number")
    search_fields = ("email", "phone", "first_name", "last_name", "inn")
    inlines = (
        TravelersInline,
        DocumentsInline,
    )

    # def get_fio(self, object):
    #     if object.user:
    #         return f"{object.user.first_name} {object.user.last_name}"

    # get_fio.short_description = "ФИО"

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "status",
                    "surcharge",
                    "request_number",
                    "user",
                    "first_name",
                    "last_name",
                    "phone",
                    "email",
                    "gender",
                    "dateofborn",
                    "city",
                    "country",
                    "bonuses",
                    "agreement",
                    "instagram"
                )
            },
        ),
        (
            _("Информация о туре"),
            {"fields": ("operatorlink", "tourid", "price", "currency")},
        ),
        (
            _("Паспортные данные"),
            {
                "fields": (
                    "passport_front",
                    "passport_back",
                    "passport_id",
                    "inn",
                    "issued_by",
                    "date_of_issue",
                    "validity",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "user",
                    "price",
                    "currency",
                    "tourid",
                    "surcharge",
                    "first_name",
                    "last_name",
                    "gender",
                    "dateofborn",
                    "phone",
                    "email",
                    "inn",
                    "passport_id",
                    "date_of_issue",
                    "validity",
                    "issued_by",
                    "city",
                    "country",
                    "passport_front",
                    "passport_back"
                ),
            },
        ),
    )

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)


@admin.register(Payments)
class PaymentsAdmin(admin.ModelAdmin):
    model = Payments
    list_display = ("id", "bank_name")
    list_display_links = list_display


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "question",
    )
    list_display_links = list_display
