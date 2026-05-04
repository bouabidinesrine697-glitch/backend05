from django.db import models


class Zone(models.Model):
    nom = models.CharField(max_length=100, unique=True) 
    latitude = models.FloatField() 
    longitude = models.FloatField()  
    nombre_trottinettes = models.IntegerField(default=0 ,null=True, blank=True)  
    duree_moyenne_location = models.FloatField(default=0 ,null=True, blank=True)  
    distance_centre = models.FloatField(default=0)  
    def nombre_disponibles(self):
        return self.trottinettes.filter(status='disponible').count()


    def __str__(self):
        return self.nom
# Create your models here.
