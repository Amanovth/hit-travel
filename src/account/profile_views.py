import os
import shutil
import requests
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from .serializers import *
from src.search.services import get_isfavorite


class UpdateProfilePhotoAPIView(APIView):
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


class RemoveProfilePhotoAPIView(APIView):
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


class ProfileInfoAPIView(APIView):
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


class UpdateInfoView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = UpdateInfoSerializer(instance=user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"response": True, "message": "Успешно обновлено"})
        return Response({"response": False})


class DeleteProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        user.delete()
        return Response({"response": True, "message": "Пользователь успешно удален"})


class MyTourAPIVIew(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        authlogin = settings.AUTHLOGIN
        authpass = settings.AUTHPASS
        user = request.user

        queryset = RequestTour.objects.filter(user=request.user)
        serializer = TourRequestSerializer(queryset, many=True)
        response = []

        for i in serializer.data:
            tourid = i["tourid"]
            tourrequest_id = i["id"]
            status = RequestTour.objects.get(tourid=tourid, user=request.user)
            detail = requests.get(
                f"http://tourvisor.ru/xml/actualize.php?tourid={tourid}&request=0"
                f"&format=json&authpass={authpass}&authlogin={authlogin}"
            )

            if detail.status_code != 200:
                continue
            try:
                d = {}
                # d["link"] = f"https://hit-travel.org/profile/agreement-pdf/{tourrequest_id}"
                d["link"] = f"http://hit-travel.org{i['agreement']}"
                d["tourid"] = tourid
                d["status"] = status.status
                d["isfavorite"] = get_isfavorite(user=user, tourid=tourid)
                d["tour"] = detail.json()["data"]["tour"]
                d["documents"] = i["documents"]
                response.append(d)
            except KeyError:
                continue

        return Response(response)


class BonusHistoryAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
        except ObjectDoesNotExist:
            return Response(
                {"response": False, "detail": "Пользователь не найден"},
                status=status.HTTP_404_NOT_FOUND,
            )

        bonus_history = requests.get(
            f"https://api.u-on.ru/{settings.KEY}/bcard-bonus-by-card/{user.bcard_id}.json"
        )

        if bonus_history.status_code != 200:
            return Response({"response": False})

        data = bonus_history.json()["records"]
        data.reverse()

        return Response(data)


# class CreateAgreementPDF(APIView):
#     def get(self, request, tourrequest_id):
#         obj = TourRequest.objects.get(id=tourrequest_id)
#         date = datetime.now().strftime("%d.%m.%Y %H:%M")
#         price_word = num2words(int(obj.price), lang="ru")
#         surcharge_word = num2words(int(obj.surcharge), lang="ru")

#         context = {
#             "obj": obj,
#             "date": date,
#             "price_word": price_word,
#             "surcharge_word": surcharge_word,
#         }

#         template = get_template("index.html")
#         html = template.render(context)

#         pdf = pdfkit.from_string(html, False)

#         filename = f"agreement_pdf_{obj.request_number}.pdf"

#         obj.agreement.save(
#             f"agreement_pdf_{obj.request_number}.pdf", ContentFile(pdf), save=True
#         )

#         return Response({"agreement_url": obj.agreement.url})


class FAQAPIView(ListAPIView):
    queryset = FAQ.objects.all()
    serializer_class = FAQListSerializer
