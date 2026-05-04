from django.db import models
from client.models import Client

class Facture(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='factures')
    date_creation = models.DateField(auto_now_add=True)
    montant_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    statut = models.CharField(max_length=20, choices=[
        ('en_attente', 'En attente'),
        ('payee', 'Payée'),
        ('annulee', 'Annulée'),
    ], default='en_attente')
    description = models.TextField(blank=True)

    def __str__(self):
        return f"Facture {self.id} - {self.client}"
# Create your models here.
