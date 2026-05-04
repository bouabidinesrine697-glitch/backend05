from django.urls import path
from .views import CreateBookingView, StartRideView, ApplyPromoCodeView, ListBookingView
urlpatterns=[

   path('CreateBooking/', CreateBookingView.as_view()),
   path('StartRideView/', StartRideView.as_view()),
   path('ApplyPromo/',ApplyPromoCodeView.as_view()),
   path('list/', ListBookingView.as_view()),
   ]