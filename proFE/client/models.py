from django.db import models


class Client(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    telephone = models.CharField(max_length=20)
    ville = models.CharField(max_length=100)
    adresse = models.CharField(max_length=255)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    date_naissance = models.DateField(null=True, blank=True)
    def __str__(self):
        return self.email
# Create your models here.
