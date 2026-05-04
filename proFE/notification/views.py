from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Notification
from .serializers import NotificationSerializer

class UserNotificationView(APIView):
    def get(self, request, user_id):
        notifications = Notification.objects.filter(user_id=user_id)
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)

class MarkAsReadView(APIView):
    def post(self, request, pk):
        notification = get_object_or_404(Notification, id=pk)
        notification.is_read = True
        notification.save()
        return Response({'message': 'La notification a été marquée comme lue'})

class CreateNotificationView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        message = request.data.get('message')
        
        notification = Notification.objects.create(
            user_id=user_id,
            message=message
        )
        
        serializer = NotificationSerializer(notification)
        return Response(serializer.data)
# Create your views here.
