from django.urls import path
from .views import  UpdatePositionView, PositionHistoryView, StartTrajetView, AddPointView, EndTrajetView,NearbyTrottinetteView
urlpatterns=[
    path('UpdatePosition/', UpdatePositionView.as_view()),
    path('PositionHistory/<int:trottinette_id>/', PositionHistoryView.as_view()),
    path('StartTrajet/', StartTrajetView.as_view()),
    path('AddPoint/<int:trajet_id>/', AddPointView.as_view()),
    path('EndTrajet/<int:trajet_id>/', EndTrajetView.as_view()),
    path('NearbyTrottinette/', NearbyTrottinetteView.as_view()),
]
   