from django.shortcuts import render
from django.db import models
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Position, Trajet
from trottinette.models import Trottinette
from booking.models import Booking
import math

def distance(lat1, lon1, lat2, lon2):

    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    return R * 2 * math.asin(math.sqrt(a))

class UpdatePositionView(APIView):
    def post(self, request):
        trottinette_id = request.data.get('trottinette_id')
        lat = request.data.get('latitude')
        lng = request.data.get('longitude')
        
        if not all([trottinette_id, lat, lng]):
            return Response({'error': 'جميع الحقول مطلوبة'}, status=400)
        
        trottinette = get_object_or_404(Trottinette, id=trottinette_id)
        Position.objects.create(
            trottinette=trottinette,
            latitude=lat,
            longitude=lng
        )
        
        trottinette.latitude = lat
        trottinette.longitude = lng
        trottinette.save()
        
        return Response({'message': 'localisation trouveé'})


class PositionHistoryView(APIView):
    def get(self, request, trottinette_id):
        trottinette = get_object_or_404(Trottinette, id=trottinette_id)
        positions = Position.objects.filter(trottinette=trottinette).order_by('-timestamp')[:20]
        
        data = [{
            'lat': p.latitude,
            'lng': p.longitude,
            'time': p.timestamp
        } for p in positions]
        
        return Response(data)

class StartTrajetView(APIView):
    def post(self, request):
        booking_id = request.data.get('booking_id')
        lat = request.data.get('start_lat')
        lng = request.data.get('start_lng')
        
        booking = get_object_or_404(Booking, id=booking_id)
        
        trajet = Trajet.objects.create(
            booking=booking,
            points=[{'lat': lat, 'lng': lng, 'time': 'now'}]
        )
        
        return Response({'trajet_id': trajet.id})


class AddPointView(APIView):
    def post(self, request, trajet_id):
        trajet = get_object_or_404(Trajet, id=trajet_id)
        lat = request.data.get('lat')
        lng = request.data.get('lng')
        
        trajet.points.append({'lat': lat, 'lng': lng, 'time': 'now'})
        trajet.save()
        
        return Response({'message': 'تمت الإضافة'})


class EndTrajetView(APIView):
    def post(self, request, trajet_id):
        trajet = get_object_or_404(Trajet, id=trajet_id)
        end_lat = request.data.get('end_lat')
        end_lng = request.data.get('end_lng')
        
       
        trajet.points.append({'lat': end_lat, 'lng': end_lng, 'time': 'now'})
        
        
        total = 0
        for i in range(len(trajet.points) - 1):
            p1 = trajet.points[i]
            p2 = trajet.points[i + 1]
            total += distance(p1['lat'], p1['lng'], p2['lat'], p2['lng'])
        
        trajet.distance_km = round(total, 2)
        trajet.save()
        
        return Response({'distance': trajet.distance_km})


class NearbyTrottinetteView(APIView):
    def get(self, request):
        lat = float(request.GET.get('lat', 0))
        lng = float(request.GET.get('lng', 0))
        radius = float(request.GET.get('radius', 5))  
        if not lat or not lng:
            return Response({'error': 'الموقع مطلوب'}, status=400)
        
        trottinette = Trottinette.objects.filter(status='disponible', battery__gt=20)
        
        result = []
        for s in trottinette:
            if s.latitude and s.longitude:
                dist = distance(lat, lng, s.latitude, s.longitude)
                if dist <= radius:
                    result.append({
                        'id': s.id,
                        'model': s.model,
                        'battery': s.battery,
                        'distance': round(dist, 2),
                        'lat': s.latitude,
                        'lng': s.longitude,
                        'price': float(s.price_per_minute)
                    })
        result.sort(key=lambda x: x['distance'])
        
        return Response(result[:10])
# Create your views here.
