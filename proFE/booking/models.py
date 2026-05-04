from django.db import models
from accounts.models import User
from trottinette.models import Trottinette

class PromoCode(models.Model):
    code = models.CharField(max_length=20, unique=True)
    discount_percent = models.IntegerField() 
    active = models.BooleanField(default=True)
    expiration_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.code

class Booking(models.Model):
    STATUS_CHOICES = [
       ('en_attente', 'En attente'),
       ('confirmée', 'Confirmée'),
       ('annulée', 'Annulée'),
       ('terminée', 'Terminée'),
]
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    trottinette=models.ForeignKey(Trottinette, on_delete=models.CASCADE)
    start_time=models.DateTimeField()
    end_time=models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='en_attente')
    def __str__(self):
        return f"{self.user} - {self.trottinette}"

class Ride(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True)
    distance = models.FloatField(default=0)
    cost = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    is_paid = models.BooleanField(default=False)
    promo_code = models.ForeignKey(PromoCode, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"Course {self.id}"


# Create your models here.
