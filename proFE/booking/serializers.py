from rest_framework import serializers
from .models import Booking, Ride, PromoCode
from accounts.models import User
class PromoCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model= PromoCode
        fields="__all__"
        
class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model= Booking
        fields="__all__"

class RideSerializer(serializers.ModelSerializer):
    class Meta:
        model= Ride
        fields="__all__"