from rest_framework import serializers
from .models import Trottinette, Maintenance, TrottinetteBooking
from accounts.models import User
from django.utils import timezone
from accounts.serializers import UserSerializer

class TrottineteSerializer(serializers.ModelSerializer):
    class Meta:
        model= Trottinette
        fields="__all__"

class MaintenanceSerializer(serializers.ModelSerializer):
    class Meta:
        model= Maintenance
        fields="__all__"

class TrottinetteBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model= TrottinetteBooking
        fields="__all__"
    
    def validate_start_time(self, value):
        """Validate that start_time is not in the past"""
        if value < timezone.now():
            raise serializers.ValidationError("Le temps de démarrage ne peut pas être dans le passé")
        return value
    
    def validate_end_time(self, value):
        """Validate that end_time is not in the past"""
        if value and value < timezone.now():
            raise serializers.ValidationError("Le temps de fin ne peut pas être dans le passé")
        return value
    
    def validate(self, data):
        """Validate booking consistency"""
        # Validate that end_time is after start_time if both are provided
        if data.get('end_time') and data.get('start_time'):
            if data['end_time'] <= data['start_time']:
                raise serializers.ValidationError("Le temps de fin doit être après le temps de démarrage")
        
        # Validate trottinette exists and is available
        trottinette = data.get('Trottinette')
        if trottinette:
            if trottinette.status != 'disponible' and not self.instance:
                raise serializers.ValidationError({
                    'Trottinette': f'Trottinette non disponible. État actuel: {trottinette.status}'
                })
            
            # Validate battery level
            if trottinette.battery <= 20:
                raise serializers.ValidationError({
                    'Trottinette': f'Batterie insuffisante: {trottinette.battery}%'
                })
        
        # Validate user exists
        user = data.get('user')
        if user and not User.objects.filter(id=user.id).exists():
            raise serializers.ValidationError({
                'user': 'Utilisateur non valide'
            })
        
        return data
class TrottinetteBookingSerializer(serializers.ModelSerializer):
    trottinette_details = TrottineteSerializer(source='Trottinette', read_only=True)  
    user_details = UserSerializer(source='user', read_only=True)                        

    class Meta:
        model = TrottinetteBooking
        fields = [
            'id',
            'Trottinette',      # ID pour écriture
            'user',             # ID pour écriture
            'trottinette_details',  # ← détails pour lecture
            'user_details',         # ← détails pour lecture
            'start_time',
            'end_time',
            'total_cost',
            'status'
        ]