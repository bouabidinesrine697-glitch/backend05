from django.shortcuts import render
from rest_framework.response import Response
from .models import Booking, Ride, PromoCode
from trottinette.models import Trottinette
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from accounts.models import User
from .serializers import BookingSerializer

class CreateBookingView(APIView):
    def post(self, request):
        user_id = request.data.get("user_id")
        trottinette_id = request.data.get("trottinette_id")
        start_time = request.data.get("start_time")

        try:
            user = User.objects.get(id=user_id)
            trottinette = Trottinette.objects.get(id=trottinette_id)
        except:
            return Response({"error": "booking introuvable"}, status=404)

        booking = Booking.objects.create(
            user=user,
            trottinette=trottinette,
            start_time=start_time
        )
        return Response({
            "message": "Booking créé",
            "booking_id": booking_id
        })

class StartRideView(APIView):
    def post(self, request):
        booking_id=request.data.get("booking_id")

        try:
            booking = booking.objects.get(id=booking_id)
        except booking.DoesNotExist:
            return Response({"error": "booking introuvable"},status=404)
        ride = ride.objects.create(
            booking=booking
        )
        return Response({
            "message": "Ride démarré",
            "ride_id": ride_id
        })

class ApplyPromoCodeView(APIView):
     def post(self, request):

        ride_id = request.data.get("ride_id")
        code = request.data.get("code")

        try:
            ride = Ride.objects.get(id=ride_id)
            promo = PromoCode.objects.get(code=code, active=True)
        except:
            return Response({"error": "Promo code invalide"}, status=400)

        discount = ride.cost * promo.discount_percent / 100
        ride.cost = ride.cost - discount
        ride.promo_code = promo
        ride.save()

        return Response({
            "message": "Promo appliqué",
            "nouveau_prix": ride.cost
        })


class ListBookingView(ListAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer


# Create your views here.
