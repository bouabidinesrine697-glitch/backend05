from django.urls import path
from .views import  CreateInvoiceView, PayInvoiceView, ListInvoicesView
urlpatterns=[

   path('CreateInvoice/', CreateInvoiceView.as_view()),
   path('PayInvoice/', PayInvoiceView.as_view()),
   path('ListInvoices/',ListInvoicesView.as_view()),
   ]