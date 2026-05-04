from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Facture
from .serializers import FactureSerializer

@api_view(['POST'])
def create_facture(request):
    serializer = FactureSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def list_factures(request):
    factures = Facture.objects.all()
    serializer = FactureSerializer(factures, many=True)
    return Response(serializer.data)
# Create your views here.
