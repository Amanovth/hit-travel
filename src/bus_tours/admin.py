from django.contrib import admin
from .models import (
    BusTours,
    TourCondition,
    TourExcursions,
    TourProgram,
    Cities,
    Gallery,
    Reviews,
    Category,
)


admin.site.register(Category)


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
