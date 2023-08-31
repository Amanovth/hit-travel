import os
import shutil
import string
from random import randint, choices
from datetime import datetime, timedelta, timezone
from rest_framework import generics, status, permissions, views
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import check_password
from django.conf import settings

from ..base.utils import Util
from .serializers import *
from src.tours.models import Tour


class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterAPIViewSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()

            email = serializer.data['email']
            user = User.objects.get(email=email)
            user.verification_code_time = datetime.now()
            user.verification_code = randint(100_000, 999_999)
            user.save()

            email_body = f"Hello! {user.last_name} {user.first_name}\n\n" \
                         f"To confirm registration in the system, enter the code below:\n\n" \
                         f"{user.verification_code}"

            email_data = {
                'email_body': email_body,
                'email_subject': 'Confirm your registration',
                'to_email': user.email
            }

            Util.send_email(email_data)

            return Response({'response': True}, status=status.HTTP_201_CREATED)
        return Response({'response': False, 'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailAPIView(generics.GenericAPIView):
    serializer_class = VerifyEmailSerializer
    try:
        def post(self, request):
            serializer = self.serializer_class(data=request.data)

            if serializer.is_valid():
                code = serializer.data['code']
                email = serializer.data['email']

                try:
                    user = User.objects.get(email=email)

                    if user.is_verified:
                        return Response({'message': _('Account is already verified')})

                    if user.verification_code_time:
                        expiration_time = user.verification_code_time + timedelta(minutes=30)
                        expiration_time = expiration_time.replace(tzinfo=timezone.utc)
                        if datetime.now(timezone.utc) >= expiration_time:
                            user.verification_code = None
                            user.verification_code_time = None
                            user.save()
                            return Response({'error': _('Code expired!'), }, status=status.HTTP_400_BAD_REQUEST)
                        if user.verification_code == code:
                            user.is_verified = True
                            user.save()
                            return Response({'response': True, 'message': _('Activation was successful!')})
                        return Response({'response': False, 'message': _('Wrong code entered')},
                                        status=status.HTTP_400_BAD_REQUEST)
                    return Response({'response': False, 'message': _('Code expired')},
                                    status=status.HTTP_400_BAD_REQUEST)
                except ObjectDoesNotExist:
                    return Response({'response': False, 'message': _('User with this email does not exist')},
                                    status=status.HTTP_400_BAD_REQUEST)
            return Response({'response': False, 'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as error:
        print(error)


class SendAgainCodeAPIView(generics.GenericAPIView):
    serializer_class = SendAgainCodeSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            email = serializer.data['email']

            try:
                user = User.objects.get(email=email)
            except ObjectDoesNotExist:
                return Response({'message': _('User with this email does not exist')},
                                status=status.HTTP_400_BAD_REQUEST)

            if user.is_verified:
                return Response({'message': _('User is already verified')}, status=status.HTTP_400_BAD_REQUEST)

            user.verification_code = randint(100_000, 999_999)
            user.verification_code_time = datetime.now()
            user.save()

            email_body = f"Your new activation code:\n\n" \
                         f"{user.verification_code}"

            email_data = {
                'email_body': email_body,
                'email_subject': 'Confirm your registration',
                'to_email': user.email
            }

            Util.send_email(email_data)
            return Response({'response': True, 'message': _('Verification code sent successfully')},
                            status=status.HTTP_200_OK)
        return Response({'response': False, 'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(ObtainAuthToken):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        if user.is_verified:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'response': True,
                'token': token.key,
                'email': user.username,
            })
        return Response({'message': _('You are not verified')})


class LogoutAPIView(views.APIView):
    def get(self, request):
        user = request.user
        print(user)
        if user.is_authenticated:
            try:
                token = Token.objects.get(user=user)
                token.delete()
                return Response({'response': True, 'message': _('Logout successful')}, status=status.HTTP_200_OK)
            except ObjectDoesNotExist:
                return Response({'message': _('User not logged in')}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': _('User not authenticated')}, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetRequestAPIView(views.APIView):
    serializer_classe = PasswordResetRequestSerializer

    def post(self, request):
        serializer = self.serializer_classe(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
                if user.is_verified:
                    token = ''.join(choices(string.ascii_letters + string.digits, k=20))
                    user.password_reset_token = token
                    user.save()

                    reset_url = f"http://localhost:8000/auth/password-reset/{token}"

                    email_body = f"To reset you password use link below:\n\n" \
                                 f"{reset_url}"

                    email_data = {
                        'email_body': email_body,
                        'email_subject': 'Reset your password',
                        'to_email': user.email
                    }

                    Util.send_email(email_data)

                    return Response({'response': True, 'message': _('Password reset link sent successfully')},
                                    status.HTTP_200_OK)
                return Response({'resonse': True, 'message': _('You are not verified')},
                                status=status.HTTP_400_BAD_REQUEST)

            except ObjectDoesNotExist:
                return Response({'message': _('User with this email does not exist')},
                                status=status.HTTP_400_BAD_REQUEST)
        return Response({'response': False, 'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetUpdateAPIView(views.APIView):
    serializer_class = PasswordResetUpdateSerializer

    def get(self, request, token):
        try:
            user = User.objects.get(password_reset_token=token)
            if user.password_reset_token == token:
                new_password = ''.join(choices(string.ascii_letters + string.digits, k=8))
                user.set_password(new_password)
                user.password_reset_token = None
                user.save()

                email_body = f"Your new password:\n\n" \
                             f"{new_password}"

                email_data = {
                    'email_body': email_body,
                    'email_subject': 'Use your new password',
                    'to_email': user.email
                }

                Util.send_email(email_data)

                return Response({'response': True, 'message': _('New password was send to your email')},
                                status.HTTP_200_OK)

        except ObjectDoesNotExist:
            return Response({'respons': False, 'message': _('Invalid token')}, status=status.HTTP_400_BAD_REQUEST)

    # def update(self, request, token):
    #     serializer = self.serializer_class(data=request.data)
    #     if serializer.is_valid():
    #         password = serializer.validated_data['password']
    #         try:
    #             user = User.objects.get(password_reset_token=token)
    #             if user.password_reset_token == token:
    #                 user.set_password(password)
    #                 user.password_reset_token = None
    #                 user.save()
    #                 return Response({'response': True, 'message': _('Password reset successfully')},
    #                                 status=status.HTTP_200_OK)
    #             return Response('error', status=status.HTTP_400_BAD_REQUEST)
    #         except ObjectDoesNotExist:
    #             return Response({'message': _('Invalid or expired token')}, status=status.HTTP_400_BAD_REQUEST)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SetNewPasswordAPIView(generics.UpdateAPIView):
    serializer_class = SetNewPasswordSerializer

    def update(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']
            try:
                user = request.user
                if user.is_verified:
                    if check_password(old_password, user.password):
                        user.set_password(new_password)
                        user.password_reset_token = None
                        user.save()
                        return Response({'response': True}, status=status.HTTP_200_OK)
                    return Response({'message': _('Old password is incorrect!')}, status=status.HTTP_400_BAD_REQUEST)
                return Response({'message': _('You are not verified!')})

            except ObjectDoesNotExist:
                return Response({'message': _('User with this email does not exist')},
                                status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
            image_path = os.path.join(settings.MEDIA_ROOT, f'profile_photos/user_{user.pk}')
            if os.path.exists(image_path):
                shutil.rmtree(image_path)

            user.photo = 'default_profile_photo.png'
            user.save()
            return Response({'response': True, 'detail': 'Profile photo removed'}, status=status.HTTP_200_OK)
        return Response({'response': False, 'detail': 'No profile photo to remove'}, status=status.HTTP_400_BAD_REQUEST)


class ProfileInfoAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
        except ObjectDoesNotExist:
            return Response({"response": False, "detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PersonalInfoSerializer(user, context={"request": request})
        return Response({
            'response': True,
            'profile': serializer.data
        })


class AddRemoveFavoriteView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, tour_id):
        user = request.user
        try:
            tour = Tour.objects.get(pk=tour_id)
        except ObjectDoesNotExist:
            return Response({"response": False, "detail": "Tour not found"}, status=status.HTTP_404_NOT_FOUND)

        favorite, created = Favorites.objects.get_or_create(user=user, tour=tour)

        if not created:
            favorite.delete()
            return Response({"response": True, "detail": "Removed from favorites"}, status=status.HTTP_200_OK)

        return Response({"response": True, "detail": "Added to favorites"}, status=status.HTTP_200_OK)


class FavoriteToursAPIView(generics.ListAPIView):
    serializer_class = FavoriteToursSerializer

    def get_queryset(self):
        return Favorites.objects.filter(user=self.request.user).select_related('tour')
