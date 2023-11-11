from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import (
    BusTours,
    TourCondition,
    TourExcursions,
    TourProgram,
    Cities,
    Gallery,
    Reviews,
    Category,
    Travelers,
    BusTourRequest,
    Meals
)


admin.site.register(Category)
admin.site.register(Meals)


class TourProgramInline(admin.StackedInline):
    model = TourProgram
    extra = 0


class TourConditionInline(admin.StackedInline):
    model = TourCondition
    extra = 0


class TourExcursionsInline(admin.StackedInline):
    model = TourExcursions
    extra = 0


class CitiesInline(admin.StackedInline):
    model = Cities
    extra = 0


class GalleryInline(admin.StackedInline):
    model = Gallery
    extra = 0


class ReviewsInline(admin.StackedInline):
    model = Reviews
    extra = 0


@admin.register(BusTours)
class BusToursAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "nights",
        "price",
        "seats",
    )
    list_display_links = (
        "id",
        "title",
    )
    list_filter = ("meal",)
    search_fields = ("title", "description")
    inlines = (
        TourProgramInline,
        TourConditionInline,
        TourExcursionsInline,
        CitiesInline,
        GalleryInline,
    )


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "email", "tour", "created_at")
    list_display_links = ("id", "full_name")
    list_filter = ("tour",)


class TravelersInline(admin.StackedInline):
    model = Travelers
    extra = 0


@admin.register(BusTourRequest)
class BusTourRequestInlin(admin.ModelAdmin):
    list_display = ("id", "user", "tour", "status", "payment_status", "created_at")
    list_display_links = ("id", "user", "tour")
    inlines = (TravelersInline,)
    
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "request_number",
                    "status",
                    "payment_status",
                    "user",
                    "tour",
                    "first_name",
                    "last_name",
                    "phone",
                    "email",
                    "gender",
                    "dateofborn",
                    "city",
                    "country",
                )
            },
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