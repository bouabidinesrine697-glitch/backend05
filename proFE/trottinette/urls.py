from django.urls import path
from .views import (
    TrottinetteAddView,
    TrottinetteListView,
    TrottinetteDetailView,
    TrottinetteUpdateView,
    TrottinetteDeleteView,
    TrottinetteAvailableView,
    TrottinetteNearbyView,
    MaintenanceAddView,
    MaintenanceListView,
    MaintenanceByTrottinetteView,
    TrottinetteBookingAddView,
    TrottinetteBookingEndView,
    UserBookingsView,
    TrottinetteBookingList,
    TrottinetteStatsView,TrottinetteBookingUpdate,BookingConfirmView
)
app_name = 'trottinette'
urlpatterns=[
    
   path('TrottinetteAdd/', TrottinetteAddView.as_view()),
   path('TrottinetteList/', TrottinetteListView.as_view()),
   path('TrottinetteDetail/<int:pk>/',TrottinetteDetailView.as_view()),
   path('TrottinetteUpdate/<int:pk>/',TrottinetteUpdateView.as_view()),
   path('<int:pk>/delete/', TrottinetteDeleteView.as_view(), name='trottinette-delete'),
   path('TrottinetteAvailable/', TrottinetteAvailableView.as_view()),
   path('TrottinetteNearby/',TrottinetteNearbyView.as_view()),
   path('MaintenanceAdd/',MaintenanceAddView.as_view()),
   path('MaintenanceList/', MaintenanceListView.as_view()),
   path('MaintenanceByTrottinette/<int:trottinette_id>/',MaintenanceByTrottinetteView.as_view()),
   path('TrottinetteBookingAdd/',TrottinetteBookingAddView.as_view()),
   path('TrottinetteBooking/<int:booking_id>/', TrottinetteBookingEndView.as_view()),
   path('UserBooking/<int:user_id>/',UserBookingsView.as_view()),
   path('TrottinetteBookingList/', TrottinetteBookingList.as_view()),
   path('TrottinetteStats/',TrottinetteStatsView.as_view()),
   path('list/', TrottinetteListView.as_view()),
   path('trottinettebookingupdate/<int:pk>/', TrottinetteBookingUpdate.as_view()),
   path('bookingconfirm/<int:pk>/', BookingConfirmView.as_view(), name='trottinette-booking-end'),

   
   
   
]