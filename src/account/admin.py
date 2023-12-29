from typing import Any
from django import forms
from django.contrib import admin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin
from .models import *


class UserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'

class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = '__all__'


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
            {"fields": ("is_verified", "verification_code",)},
        ),
    )
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

    form = UserChangeForm
    add_form = UserCreationForm
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

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if not request.user.is_superuser:
            for fieldset in fieldsets:
                fieldset[1]['fields'] = [field for field in fieldset[1]['fields'] if field not in ['groups', 'is_staff']]
        return fieldsets


class TravelersInline(admin.StackedInline):
    model = Traveler
    extra = 0
    fields = ["first_name", "last_name"]


class DocumentsInline(admin.StackedInline):
    model = Document
    extra = 0


class TourRequestAdminForm(forms.ModelForm):
    class Meta:
        model = RequestTour
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Pre-fill the 'first_name' field based on the selected user
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name


@admin.register(RequestTour)
class TourRequestAdmin(admin.ModelAdmin):
    # form = TourRequestAdminForm
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
                    # "price",
                    # "currency",
                    # "tourid",
                    # "surcharge",
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

    autocomplete_fields = ("user", )

    



    # def save_model(self, request, obj, form, change):
    #     obj.user = request.user
    #     if obj.user:
    #         obj.first_name = obj.user.first_name
    #         obj.last_name = obj.user.last_name
    #         obj.phone = obj.user.phone 
    #         obj.email = obj.user.email
    #         obj.gender = obj.user.profile.gender
    #         obj.dateofborn = obj.user.dateofborn 

    #     obj.save()
    



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
