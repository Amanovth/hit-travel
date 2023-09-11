from datetime import datetime
from rest_framework import generics, permissions
from rest_framework.response import Response

from .models import TourRequest, OrderHistory
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
            serializer.save(user=request.user)
            
            order_history, created = OrderHistory.objects.get_or_create(
                user=user,
                tourid=serializer.data['tourid'],
            )
            
            if created:
                message = "Успешно оформлено"
            else:
                message = "Успешно оформлено, история заказов уже существует."

            res = create_lead(serializer.data, user)
            detail = False
            if res:
                detail = True
            
            return Response({"response": True, "message": message, "detail": detail})
