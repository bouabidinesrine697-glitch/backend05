from django.db import models
from accounts.models import User
from trottinette.models import Trottinette
from booking.models import Booking

class Position(models.Model): 
    trottinette = models.ForeignKey(Trottinette, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    battery_at_time = models.IntegerField(default=100)
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Position'
        verbose_name_plural = 'Positions'
    
    def __str__(self):
        return f"{self.trottinette} - {self.latitude}, {self.longitude}"


class Trajet(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='trajet')
    points = models.JSONField(default=list)  
    distance_km = models.FloatField(default=0)
    duree_minutes = models.IntegerField(default=0)
    start_position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, related_name='+')
    end_position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, related_name='+')
    
    class Meta:
        verbose_name = 'Trajet'
        verbose_name_plural = 'Trajets'
    
    def __str__(self):
        return f"Trajet {self.booking.id} - {self.distance_km}km"


class Zone(models.Model): 
    nom = models.CharField(max_length=100)
    points = models.JSONField() 
    is_active = models.BooleanField(default=True)
    vitesse_max = models.IntegerField(default=20)  
    
    class Meta:
        verbose_name = 'Zone'
        verbose_name_plural = 'Zones'
    
    def __str__(self):
        return self.nom
# Create your models here.
