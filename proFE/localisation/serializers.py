from rest_framework import serializers
from .models import Position, Trajet, Zone
from accounts.models import User
class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model= Position
        fields="__all__"
        
class TrajetSerializer(serializers.ModelSerializer):
    class Meta:
        model= Trajet
        fields="__all__"

class ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model= Zone
        fields="__all__"