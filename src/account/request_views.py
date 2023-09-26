from datetime import datetime
from rest_framework import generics, permissions
from rest_framework.response import Response

from .models import TourRequest
from .serializers import TourRequestSerializer
from .services import create_lead


class TourRequestView(generics.CreateAPIView):
    serializer_class = TourRequestSerializer
    queryset = TourRequest.objects.all()
    permission_classes = [permissions.IsAuthenticated]
        
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        user = request.user
        
        if serializer.is_valid():
            tour_id = serializer.validated_data.get('tourid')
            existing_tour_request = TourRequest.objects.filter(tourid=tour_id, user=user)
            
            if existing_tour_request.exists():
                # Удалить существующий TourRequest с тем же tourid.
                existing_tour_request.delete()
            
            serializer.save(user=request.user)

            res = create_lead(serializer.data, user)
            detail = False
            if res:
                detail = True
            
            return Response({"response": True, "detail": detail, "message": "Заявка успешно отправлено"})
        return Response(serializer.errors)
