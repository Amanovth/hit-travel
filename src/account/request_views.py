from datetime import datetime
from rest_framework import generics, permissions
from rest_framework.response import Response

from .models import TourRequest
from .serializers import TourRequestSerializer
from .services import create_lead, decrease_bonuses
from django.core.files.base import ContentFile
from django.template.loader import get_template
import pdfkit
from num2words import num2words


class TourRequestView(generics.CreateAPIView):
    serializer_class = TourRequestSerializer
    queryset = TourRequest.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        user = request.user

        if serializer.is_valid():
            tour_id = serializer.validated_data.get("tourid")
            existing_tour_request = TourRequest.objects.filter(
                tourid=tour_id, user=user
            )

            if existing_tour_request.exists():
                return Response({"response": False})

            serializer.save(user=request.user)

            res = create_lead(serializer.data, user)
            if res:
                tour_request = TourRequest.objects.get(tourid=tour_id, user=user)
                tour_request.request_number = res["id"]

                date = datetime.now().strftime("%d.%m.%Y %H:%M")
                price_word = num2words(int(tour_request.price), lang="ru")
                surcharge_word = num2words(int(tour_request.surcharge), lang="ru")

                context = {
                    "obj": tour_request,
                    "date": date,
                    "price_word": price_word,
                    "surcharge_word": surcharge_word,
                }

                template = get_template("index.html")
                html = template.render(context)

                pdf = pdfkit.from_string(html, False)

                tour_request.agreement.save(
                    f"agreement_pdf_{tour_request.request_number}.pdf",
                    ContentFile(pdf),
                    save=True,
                )

                tour_request.save()

                bonuses = decrease_bonuses(
                    user.bcard_id, serializer.data["bonuses"], "test"
                )

            return Response(
                {
                    "response": True,
                    "message": "Заявка успешно отправлено",
                    "requestid": tour_request.id,
                }
            )
        return Response(serializer.errors)
