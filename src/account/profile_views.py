import os
import shutil
from rest_framework import generics, permissions, views, status
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from .serializers import *


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
                settings.MEDIA_ROOT, f"profile_photos/{user.photo}"
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


class UpdateInfoView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, *args, **kwargs):
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
