from django.urls import path
from .views import ClientCreateView, ClientListView, ClientRegistrationView, ClientLoginView,  ClientDeleteView, ClientDetailView

urlpatterns = [
    path('clients/add/', ClientCreateView.as_view()),
    path('clients/', ClientListView.as_view()),
    path('clients/register/', ClientRegistrationView.as_view()),
    path('clients/login/', ClientLoginView.as_view()),
    path('<int:client_id>/delete/', ClientDeleteView.as_view(), name='client-delete'),
    path('clients/<int:client_id>/', ClientDetailView.as_view()),
]