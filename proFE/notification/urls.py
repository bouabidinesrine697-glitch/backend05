from django.urls import path
from .views import UserNotificationView, MarkAsReadView, CreateNotificationView

urlpatterns = [
    path('UserNotification/<int:user_id>/', UserNotificationView.as_view()),
    path('MarkAsRead/<int:pk>/', MarkAsReadView.as_view()),
    path('CreateNotification/', CreateNotificationView.as_view()),
    ]