import os
import shutil
import string
import requests
from random import randint, choices
from datetime import datetime, timedelta, timezone
from rest_framework import generics, status, permissions, views
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import check_password
from django.conf import settings

from ..base.utils import Util
from .serializers import *


class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterAPIViewSerializer

    def add_tourist(self, user):
        crm_data = {
            "u_surname": user.last_name,
            "u_name": user.first_name,
            "u_email": user.email,
            "u_phone": user.phone,
        }

        key = settings.KEY
        res = requests.post(
            f"https://api.u-on.ru/{key}/user/create.json", data=crm_data
        )
        res.raise_for_status()
        user.tourist_id = res.json()["result"]
        user.save()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        """ Register user in system
        """
        if serializer.is_valid():
            email = serializer.data["email"]
            first_name = serializer.data["first_name"]
            last_name = serializer.data["last_name"]
            password = serializer.data["password"]
            confirm_password = serializer.data["confirm_password"]
            phone = serializer.data["phone"]

            if User.objects.filter(email=email).exists():
                return Response(
                    {
                        "response": False,
                        "message": "Пользователь с таким email уже существует.",
                    }
                )

            if password != confirm_password:
                return Response(
                    {"response": False, "password": _("Пароли не совпадают.")}
                )

            user = User(
                email=email, first_name=first_name, last_name=last_name, phone=phone
            )
            user.set_password(password)
            user.save()

            user.verification_code_time = datetime.now()
            user.verification_code = randint(100_000, 999_999)
            user.save()

            """ Create tourist in https://u-on.ru
            """
            self.add_tourist(user)

            """ Send verification code to user
            """
            email_body = (
                f"Привет! {user.last_name} {user.first_name}\n\n"
                f"Для подтверждения регистрации в системе введите код ниже:\n\n"
                f"{user.verification_code}"
            )

            email_data = {
                "email_body": email_body,
                "email_subject": "Подтвердите регистрацию",
                "to_email": user.email,
            }

            Util.send_email(email_data)

            return Response({"response": True}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)


class VerifyEmailAPIView(generics.GenericAPIView):
    serializer_class = VerifyEmailSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            code = serializer.data["code"]
            email = serializer.data["email"]

            try:
                user = User.objects.get(email=email)

                if user.is_verified:
                    return Response({"message": _("Аккаунт уже подтвержден")})

                if user.verification_code_time:
                    expiration_time = user.verification_code_time + timedelta(
                        minutes=30
                    )
                    expiration_time = expiration_time.replace(tzinfo=timezone.utc)

                    if datetime.now(timezone.utc) >= expiration_time:
                        user.verification_code = None
                        user.verification_code_time = None
                        user.save()
                        return Response(
                            {
                                "reponse": False,
                                "message": _("Срок действия кода истек!"),
                            }
                        )
                    if user.verification_code == code:
                        user.is_verified = True
                        user.save()
                        return Response(
                            {
                                "response": True,
                                "message": _("Верификация прошла успешно!"),
                            }
                        )
                    return Response(
                        {"response": False, "message": _("Введен неверный код")}
                    )
                return Response(
                    {"response": False, "message": _("Срок действия кода истек!")}
                )
            except ObjectDoesNotExist:
                return Response(
                    {
                        "response": False,
                        "message": _("Пользователь с таким email не существует"),
                    }
                )
        return Response(
            {"response": False, "detail": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class SendAgainCodeAPIView(generics.GenericAPIView):
    serializer_class = SendAgainCodeSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            email = serializer.data["email"]

            try:
                user = User.objects.get(email=email)
            except ObjectDoesNotExist:
                return Response(
                    {
                        "reponse": False,
                        "message": _("Пользователь с таким email не существует"),
                    },
                )

            user.verification_code = randint(100_000, 999_999)
            user.verification_code_time = datetime.now()
            user.save()

            email_body = f"Ваш новый код активации:\n\n" f"{user.verification_code}"

            email_data = {
                "email_body": email_body,
                "email_subject": "Подтвердите регистрацию",
                "to_email": user.email,
            }

            Util.send_email(email_data)
            return Response(
                {"response": True, "message": _("Код подтверждения успешно отправлен")}
            )
        return Response(
            {"response": False, "detail": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class LoginAPIView(ObtainAuthToken):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        try:
            user = serializer.validated_data["user"]
        except KeyError:
            return Response(
                {
                    "resonse": False,
                    "message": "Невозможно войти в систему с указанными учетными данными",
                }
            )
        if user.is_verified:
            token, created = Token.objects.get_or_create(user=user)
            return Response(
                {
                    "response": True,
                    "token": token.key,
                    "email": user.email,
                }
            )
        return Response({"response": False, "message": _("Вы не верифицированы")})


class LogoutAPIView(views.APIView):
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            try:
                token = Token.objects.get(user=user)
                token.delete()
                return Response(
                    {"response": True, "message": _("Выход выполнен успешно")}
                )
            except ObjectDoesNotExist:
                return Response(
                    {"reponse": False, "message": _("Пользователь не авторизован")}
                )
        return Response(
            {"response": False, "message": _("Пользователь не авторизован")}
        )


class PasswordResetRequestAPIView(views.APIView):
    serializer_classe = PasswordResetRequestSerializer

    def post(self, request):
        serializer = self.serializer_classe(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            try:
                user = User.objects.get(email=email)
                if user.is_verified:
                    token = "".join(choices(string.ascii_letters + string.digits, k=20))
                    user.password_reset_token = token
                    user.save()

                    reset_url = (
                        f"http://77.232.128.174:8000/auth/password-reset/{token}"
                    )

                    email_body = (
                        f"Для сброса пароля используйте ссылку ниже:\n\n" f"{reset_url}"
                    )

                    email_data = {
                        "email_body": email_body,
                        "email_subject": "Сбросить пароль",
                        "to_email": user.email,
                    }

                    Util.send_email(email_data)

                    return Response(
                        {
                            "response": True,
                            "message": _("Ссылка для сброса пароля успешно отправлена"),
                        }
                    )
                return Response({"resonse": True, "message": _("Вы не верифицированы")})

            except ObjectDoesNotExist:
                return Response(
                    {"message": _("Пользователь с таким адресом email не существует")},
                )
        return Response(
            {"response": False, "detail": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class PasswordResetUpdateAPIView(views.APIView):
    serializer_class = PasswordResetUpdateSerializer

    def get(self, request, token):
        try:
            user = User.objects.get(password_reset_token=token)
            if user.password_reset_token == token:
                new_password = "".join(
                    choices(string.ascii_letters + string.digits, k=8)
                )
                user.set_password(new_password)
                user.password_reset_token = None
                user.save()

                email_body = f"Ваш новый пароль:\n\n" f"{new_password}"

                email_data = {
                    "email_body": email_body,
                    "email_subject": "Используйте новый пароль",
                    "to_email": user.email,
                }

                Util.send_email(email_data)

                return Response(
                    {
                        "response": True,
                        "message": _(
                            "Новый пароль был отправлен на вашу электронную почту"
                        ),
                    }
                )

        except ObjectDoesNotExist:
            return Response({"respons": False, "message": _("Неверный токен")})


class SetNewPasswordAPIView(generics.UpdateAPIView):
    serializer_class = SetNewPasswordSerializer

    def update(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            old_password = serializer.validated_data["old_password"]
            new_password = serializer.validated_data["new_password"]

            user = get_object_or_404(User, pk=request.user.pk)

            if not user.is_verified or not user.is_authenticated:
                return Response(
                    {"reponse": False, "message": "Вы неавторизованы"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            if not check_password(old_password, user.password):
                return Response(
                    {"response": False, "message": _("Старый пароль неверен!")}
                )

            user.set_password(new_password)
            user.save()
            return Response({"response": True, "message": _("Пароль успешно обновлен")})
        return Response(
            {"response": False, "detail": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class UpdateProfilePhotoAPIView(generics.UpdateAPIView):
    serializer_class = UpdateProfilePhotoSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class RemoveProfilePhotoAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user

        if user.photo:
            image_path = os.path.join(
                settings.MEDIA_ROOT, f"profile_photos/user_{user.pk}"
            )
            if os.path.exists(image_path):
                shutil.rmtree(image_path)

            user.photo = "default_profile_photo.png"
            user.save()
            return Response(
                {"response": True, "message": "Фотография профиля удалена."}
            )
        return Response(
            {
                "response": False,
                "messafe": "Нет фотографии профиля, которую можно удалить.",
            }
        )


class ProfileInfoAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
        except ObjectDoesNotExist:
            return Response(
                {"response": False, "detail": "Пользователь не найден"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = PersonalInfoSerializer(user, context={"request": request})
        return Response({"response": True, "data": serializer.data})


class OrderHistoryView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        authlogin = settings.AUTHLOGIN
        authpass = settings.AUTHPASS

        queryset = OrderHistory.objects.filter(user=request.user)
        serializer = OrderHistoryToursSerializer(queryset, many=True)
        response = []

        for i in serializer.data:
            detail = requests.get(
                f"http://tourvisor.ru/xml/actualize.php?tourid={i['tourid']}&request=0"
                f"&format=json&authpass={authpass}&authlogin={authlogin}"
            )
            detail.raise_for_status()
            flights = requests.get(
                f"http://tourvisor.ru/xml/actdetail.php?tourid={i['tourid']}"
                f"&format=json&authpass={authpass}&authlogin={authlogin}"
            )
            flights.raise_for_status()
            
            d = {}
            d['data'] = detail.json()['data']
            try:
                d['flights'] = flights.json()['flights']
            except KeyError:
                d['flights'] = flights.json()
            response.append(d)
            
        return Response(response)