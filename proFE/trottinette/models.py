from django.db import models
from accounts.models import User
from cloudinary.models import CloudinaryField


class Trottinette(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    QR_code = models.CharField(max_length=50, unique=True)
    model = models.CharField(max_length=50)
    status = models.CharField(max_length=20, default='disponible')
    price_per_minute = models.FloatField(null=True)
    battery = models.IntegerField(default=100)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    image = CloudinaryField('image', null=True, blank=True)
    image_url = models.URLField(max_length=200, null=True, blank=True)
    zone = models.ForeignKey('zone.Zone', on_delete=models.SET_NULL, null=True, blank=True, related_name='trottinette')

    def __str__(self):
        return f"{self.model} - {self.QR_code}"


class Maintenance(models.Model):
    id = models.AutoField(primary_key=True)
    Trottinette = models.ForeignKey(Trottinette, on_delete=models.CASCADE)
    discription = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Maintenance {self.Trottinette} - {self.date}"


class TrottinetteBooking(models.Model):
    STATUS_CHOICES = [
        ('en_attente', 'En attente'),
        ('confirmée', 'Confirmée'),
        ('refusée', 'Refusée'),
        ('terminée', 'Terminée'),
    ]

    Trottinette = models.ForeignKey(Trottinette, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    total_cost = models.FloatField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='en_attente')

    def __str__(self):
        return f"{self.user} - {self.Trottinette}"
