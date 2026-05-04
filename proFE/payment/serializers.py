from rest_framework import serializers
from .models import Invoice, Transaction
from accounts.models import User
class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model= Invoice
        fields="__all__"
        
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model= Transaction
        fields="__all__"