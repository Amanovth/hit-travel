import locale
from rest_framework import serializers
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate

from .models import *


locale.setlocale(locale.LC_TIME, "ru_RU.UTF-8")


class RegisterAPIViewSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(required=True, max_length=68, min_length=8)

    class Meta:
        model = User
        fields = [
            "email",
            "phone",
            "first_name",
            "last_name",
            "password",
            "confirm_password",
        ]

    def validate(self, attrs):
        email = attrs.get("email")

        if User.objects.filter(email=email).exists():
            return Response(
                {
                    "response": False,
                    "message": _("Пользователь с таким email уже существует."),
                }
            )

        return attrs


class VerifyEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.IntegerField()

    class Meta:
        fields = ["email", "code"]


class SendAgainCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()

    class Meta:
        fields = ["email"]


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(
        label=_("Email"), style={"input_type": "email"}, write_only=True
    )
    password = serializers.CharField(
        label=_("Password"),
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
    )
    token = serializers.CharField(label=_("Token"), read_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(
                request=self.context.get("request"), username=email, password=password
            )

            if not user:
                return Response(
                    {
                        "response": False,
                        "message": "Невозможно войти в систему с указанными учетными даннымиpDvT#uJwi4+LNU",
                    }
                )
        else:
            msg = _("Должен включать имя пользователя и пароль")
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    class Meta:
        fields = ["email"]


class PasswordResetUpdateSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        fields = ["password", "confirm_password"]

    def validate(self, attrs):
        password = attrs.get("password")
        confirm_password = attrs.get("confirm_password")

        if password != confirm_password:
            raise serializers.ValidationError("Пароли не совпадают")
        return attrs


class SetNewPasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        fields = ["old_password", "new_password", "confirm_password"]

    def validate(self, attrs):
        new_password = attrs.get("new_password")
        confirm_password = attrs.get("confirm_password")

        if new_password != confirm_password:
            raise serializers.ValidationError({"error": "Пароли не совпадают"})
        return attrs


class UpdateProfilePhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["photo"]


class BonusHistorySerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    valid = serializers.SerializerMethodField()

    class Meta:
        model = BonusHistory
        fields = ["id", "name", "sum", "currency", "created_at", "valid"]

    def get_created_at(self, obj):
        return obj.created_at.strftime("%d %B %Y %H:%M")

    def get_valid(self, obj):
        return obj.valid.strftime("%d %B %Y")


class PersonalInfoSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()
    date_joined = serializers.SerializerMethodField()
    last_login = serializers.SerializerMethodField()
    bonus_history = BonusHistorySerializer(many=True)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone",
            "date_joined",
            "last_login",
            "photo",
            "balance",
            "bonuses",
            "bonus_history",
        ]

    def get_photo(self, obj):
        if obj.photo:
            request = self.context.get("request")
            photo_url = obj.photo.url
            return request.build_absolute_uri(photo_url)
        return None

    def get_date_joined(self, obj):
        return obj.date_joined.strftime("%Y/%m/%d %H:%M")

    def get_last_login(self, obj):
        if obj.last_login:
            return obj.last_login.strftime("%Y/%m/%d %H:%M")


class OrderHistoryToursSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderHistory
        fields = "__all__"


class UpdateInfoSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ["first_name", "last_name"]


class TourRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourRequest
        fields = [
            "first_name",
            "last_name",
            "phone",
            "email",
            "gender",
            "citizenship",
            "inn",
            "tourid",
        ]
