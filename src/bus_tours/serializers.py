from rest_framework import serializers

from .models import (
    BusTours,
    TourProgram,
    TourCondition,
    TourExcursions,
    Cities,
    Gallery,
    Reviews,
    Category,
)


class TourReviewsSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = Reviews
        fields = ["full_name", "email", "created_at", "body"]

    def get_created_at(self, obj):
        if obj.created_at:
            return obj.created_at.strftime("%d.%m.%Y")
        return None


class BusTourListSerializer(serializers.ModelSerializer):
    meal = serializers.ReadOnlyField(source="meal.name")
    mealname = serializers.ReadOnlyField(source="meal.russian")
    img = serializers.SerializerMethodField()
    total_reviews = serializers.SerializerMethodField()
    reviews = TourReviewsSerializer(many=True)

    class Meta:
        model = BusTours
        fields = [
            "id",
            "title",
            "seats",
            "datefrom",
            "dateto",
            "nights",
            "days",
            "meal",
            "mealname",
            "price",
            "img",
            "total_reviews",
            "reviews",
        ]

    def get_img(self, obj):
        images = obj.gallery.all()
        if images:
            return f"https://hit-travel.org{images[0].img.url}"
        return None

    def get_total_reviews(self, obj):
        return obj.reviews.count()


class TourProgramsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourProgram
        fields = ["day", "title", "body"]


class TourConditionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourCondition
        fields = ["title", "body"]


class TourExcursionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourExcursions
        fields = ["title", "body"]


class CitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cities
        fields = ["name"]


class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = ["img"]


class BusTourDetailSerializer(serializers.ModelSerializer):
    meal = serializers.ReadOnlyField(source="meal.name")
    meal_fullname = serializers.ReadOnlyField(source="meal.fullname")
    meal_russian = serializers.ReadOnlyField(source="meal.russian")
    meal_russianfull = serializers.ReadOnlyField(source="meal.russianfull")
    programs = TourProgramsSerializer(many=True)
    conditions = TourConditionsSerializer(many=True)
    excursions = TourExcursionsSerializer(many=True)
    cities = CitiesSerializer(many=True)
    gallery = GallerySerializer(many=True)
    reviews = TourReviewsSerializer(many=True)
    isbustour = serializers.SerializerMethodField()

    class Meta:
        model = BusTours
        fields = [
            "id",
            "title",
            "seats",
            "datefrom",
            "dateto",
            "nights",
            "days",
            "meal",
            "meal_fullname",
            "meal_russian",
            "meal_russianfull",
            "price",
            "description",
            "description_pdf",
            "programs",
            "conditions",
            "excursions",
            "cities",
            "gallery",
            "reviews",
            "isbustour",
        ]

    def get_isbustour(self, obj):
        return True


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = ["tour", "full_name", "email", "body"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
