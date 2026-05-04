from django.db import models
from accounts.models import User
from trottinette.models import TrottinetteBooking

class Invoice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    TrottinetteBooking = models.OneToOneField(TrottinetteBooking, on_delete=models.CASCADE, null=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=20, default='en_attente')
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(null=True)
    
    def __str__(self):
        return f"{self.invoice_number} - {self.amount} DT"


class Transaction(models.Model):
    transaction_id = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    invoice = models.ForeignKey(Invoice, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    payment_method = models.CharField(max_length=20)
    status = models.CharField(max_length=20, default='en_attente')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.transaction_id} - {self.amount} DT"
# Create your models here.
