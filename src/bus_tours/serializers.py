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
    Travelers,
    BusTourRequest,
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
    isrequested = serializers.SerializerMethodField()

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
            "isrequested",
        ]

    def get_isbustour(self, obj):
        return True

    def get_isrequested(self, obj):
        user = self.context["request"].user
        if user.is_authenticated:
            tour = obj
            request_exists = BusTourRequest.objects.filter(user=user, tour=tour).exists()
            return request_exists
        return False


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = ["tour", "full_name", "email", "body"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class TravelerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Travelers


class BusTourRequestSerializer(serializers.ModelSerializer):
    bustour_travelers = TravelerSerializer(many=True, required=False)
    passport_front = serializers.FileField(allow_empty_file=True, required=False)
    passport_back = serializers.FileField(allow_empty_file=True, required=False)
    datefrom = serializers.ReadOnlyField(source="tour.datefrom")
    dateto = serializers.ReadOnlyField(source="tour.dateto")
    nights = serializers.ReadOnlyField(source="tour.nights")
    price = serializers.ReadOnlyField(source="tour.price")
    num_of_tourists = serializers.ReadOnlyField(source="tour.num_of_tourists")
    meal = serializers.ReadOnlyField(source="tour.meal.name")

    class Meta:
        model = BusTourRequest
        fields = [
            "tour",
            "first_name",
            "last_name",
            "email",
            "phone",
            "gender",
            "dateofborn",
            "inn",
            "passport_id",
            "date_of_issue",
            "issued_by",
            "validity",
            "city",
            "country",
            "passport_front",
            "passport_back",
            "bustour_travelers",
            "datefrom",
            "dateto",
            "nights",
            "price",
            "num_of_tourists",
            "meal",
        ]

    def create(self, validated_data):
        try:
            travelers_list = validated_data.pop("bustour_travelers")
            instance = BusTourRequest.objects.create(**validated_data)
            for traveler in travelers_list:
                instance.bustour_travelers.create(**traveler)
            return instance
        except KeyError:
            return super().create(validated_data)
