from django.urls import path
from . import views

urlpatterns = [
    path('factures/', views.list_factures),
    path('factures/add/', views.create_facture),
]