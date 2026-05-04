from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Zone
from .serializers import ZoneSerializer,TrottinetteMiniSerializer
class ZoneCreateView(APIView):
    def post(self, request):
        print(request.data)
        serializer = ZoneSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class ZoneListCreate(APIView):
    def get(self, request):
        zones = Zone.objects.all()
        serializer = ZoneSerializer(zones, many=True)
        return Response(serializer.data)


class ZoneDetail(APIView):
    def get_object(self, pk):
        try:
            return Zone.objects.get(pk=pk)
        except Zone.DoesNotExist:
            return None

    def get(self, request, pk):
        zone = self.get_object(pk)
        if zone is None:
            return Response({"error": "Zone not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ZoneSerializer(zone)
        return Response(serializer.data)

    def put(self, request, pk):
        zone = self.get_object(pk)
        if zone is None:
            return Response({"error": "Zone not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ZoneSerializer(zone, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        zone = self.get_object(pk)
        if zone is None:
            return Response({"error": "Zone not found"}, status=status.HTTP_404_NOT_FOUND)
        zone.delete()
        return Response({"message": "Zone deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Zone
from trottinette.models import Trottinette
from django.db.models import Count, Q

class ZoneDisponiblesView(APIView):
    def get(self, request):
        data = []
        zones = Zone.objects.all()
        for zone in zones:
            trottinettes = Trottinette.objects.filter(zone=zone)
            total = trottinettes.count()
            disponibles = trottinettes.filter(status='disponible').count()
            serializer = TrottinetteMiniSerializer(trottinettes, many=True)
            data.append({
                'id': zone.id,
                'nom': zone.nom,
                'longitude': zone.longitude,
                'latitude': zone.latitude,
                'nombre_total': total,
                'nombre_disponibles': disponibles,
                'trottinettes': serializer.data  
            })

        return Response(data)
