from django.urls import path
from .views import  ZoneCreateView,  ZoneListCreate, ZoneDetail, ZoneDisponiblesView

urlpatterns = [
    path('zones-create/', ZoneCreateView.as_view(), name='zone-list-create'),
    path('zones/', ZoneListCreate.as_view(), name='zone-list-create'),
    path('<int:pk>/', ZoneDetail.as_view(), name='zone-detail'),
    path('zones-disponible/',ZoneDisponiblesView.as_view(),name='Zone-Disponibles'),
]