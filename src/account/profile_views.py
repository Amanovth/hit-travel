import os
import shutil
import requests
from rest_framework import generics, permissions, views, status
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.shortcuts import get_list_or_404
from .serializers import *


class UpdateProfilePhotoAPIView(views.APIView):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = UpdateProfilePhotoSerializer(
            instance=request.user, data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response({"response": True, "message": "Успешно обновлено"})
        return Response({"response": False})


class RemoveProfilePhotoAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user

        if user.photo:
            image_path = os.path.join(
                settings.MEDIA_ROOT, f"profile_photos/{user.photo}"
            )
            if os.path.exists(image_path):
                shutil.rmtree(image_path)

            user.photo = "default.png"
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


class UpdateInfoView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = UpdateInfoSerializer(instance=user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"response": True, "message": "Успешно обновлено"})
        return Response({"response": False})


class DeleteProfileView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        user = request.user
        user.delete()
        return Response({"response": True, "message": "Пользователь успешно удален"})


class MyTourAPIVIew(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        authlogin = settings.AUTHLOGIN
        authpass = settings.AUTHPASS

        queryset = TourRequest.objects.filter(user=request.user)
        serializer = TourRequestSerializer(queryset, many=True)
        response = []

        for i in serializer.data:
            tourid = i['tourid']
            status = TourRequest.objects.get(tourid=tourid, user=request.user)
            detail = requests.get(
                f"http://tourvisor.ru/xml/actualize.php?tourid={tourid}&request=0"
                f"&format=json&authpass={authpass}&authlogin={authlogin}"
            )

            if detail.status_code != 200:
                continue
            d = {}
            d["tourid"] = tourid
            d["status"] = status.status
            d["tour"] = detail.json()["data"]["tour"]
            response.append(d)

        return Response(response)
