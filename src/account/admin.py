from typing import Any
from django import forms
from django.contrib import admin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin
from .models import *
from .services import permissions


@admin.register(User)
class UserAdmin(UserAdmin):
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
    filter_horizontal = ()

    fieldsets = [
        (
            None,
            {
                "fields": (
                    "email",
                    "password",
                    "tourist_id",
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
                    "dateofborn",
                    "gender",
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
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
        (
            _("Верификация"),
            {
                "fields": (
                    "is_verified",
                    "verification_code",
                )
            },
        ),
    ]
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "groups",
                    "is_staff",
                    "email",
                    "phone",
                    "first_name",
                    "last_name",
                    "surname",
                    "password1",
                    "password2",
                    "dateofborn",
                    "inn",
                    "passport_id",
                    "city",
                    "county",
                    "date_of_issue",
                    "validity",
                    "issued_by",
                ),
            },
        ),
    )

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if not request.user.is_superuser:
            for fieldset in fieldsets:
                fieldset[1]["fields"] = [
                    field
                    for field in fieldset[1]["fields"]
                    if field not in ["groups", "is_staff"]
                ]

        if request.user.is_superuser:
            fieldsets.append(permissions)
        return fieldsets


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
        "user",
    )
    list_editable = ("status",)
    list_filter = ("status",)
    list_display_links = ("id", "first_name", "last_name", "request_number")
    search_fields = ("email", "phone", "first_name", "last_name", "inn")
    inlines = (
        TravelersInline,
        DocumentsInline,
    )

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
                    # "first_name",
                    # "last_name",
                    # "gender",
                    # "dateofborn",
                    # "phone",
                    # "email",
                    # "inn",
                    # "passport_id",
                    # "date_of_issue",
                    # "validity",
                    # "issued_by",
                    # "city",
                    # "country",
                ),
            },
        ),
        (
            _("Информация о туре"),
            {"fields": ("operatorlink", "tourid", "price", "currency", "surcharge")},
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
