import json
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import TourRequest
from .serializers import TourRequestSerializer
from .services import create_lead, decrease_bonuses


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
                tour_request.save()
                
                bonuses = decrease_bonuses(user.bcard_id, serializer.data["bonuses"], "test")

            return Response(
                {
                    "response": True,
                    "message": "Заявка успешно отправлено",
                    "requestid": tour_request.id
                }
            )
        return Response(serializer.errors)
