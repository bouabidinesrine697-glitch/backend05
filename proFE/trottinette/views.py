from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Trottinette, Maintenance, TrottinetteBooking
from .serializers import TrottineteSerializer, MaintenanceSerializer, TrottinetteBookingSerializer
from accounts.models import User
from django.utils import timezone
import cloudinary.uploader



class TrottinetteAddView(APIView):
    def post(self, request):
        data = request.data.copy()
        if 'image' in request.FILES:
            image_file = request.FILES['image']
            result = cloudinary.uploader.upload(
                image_file,
                use_filename=True,
                unique_filename=True,
                tags=["trottinette"],
                context={
                    "app": "trottinette_app"
                }
            )
            data['image'] = result['secure_url']
            data['image_url'] = result['secure_url']
            data['image_url'] = result['secure_url']
            print("Image uploaded to Cloudinary:", result['secure_url'])    

        serializer = TrottineteSerializer(data=data)
        print(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TrottinetteListView(APIView):
    def get(self, request):
        trottinettes = Trottinette.objects.all()
        serializer = TrottineteSerializer(trottinettes, many=True)
        return Response(serializer.data)


class TrottinetteDetailView(APIView):
    def get(self, request, pk):
        try:
            trottinette = Trottinette.objects.get(id=pk)
            serializer = TrottineteSerializer(trottinette)
            return Response(serializer.data)
        except Trottinette.DoesNotExist:
            return Response({'error': 'Trottinette non disponible'}, status=status.HTTP_404_NOT_FOUND)


class TrottinetteUpdateView(APIView):
    def put(self, request, pk):
        try:
            trottinette = Trottinette.objects.get(id=pk)
            data = request.data.copy()
            if 'image' in request.FILES:
                image_file = request.FILES['image']
                result = cloudinary.uploader.upload(
                    image_file,
                    use_filename=True,
                    unique_filename=True,
                    tags=["trottinette"],
                    context={
                        "app": "trottinette_app"
                    }
                )
                data['image'] = result['secure_url']
            serializer = TrottineteSerializer(trottinette, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Trottinette.DoesNotExist:
            return Response({'error': 'Trottinette non disponible'}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, pk):
        try:
            trottinette = Trottinette.objects.get(id=pk)
            data = request.data.copy()
            if 'image' in request.FILES:
                image_file = request.FILES['image']
                result = cloudinary.uploader.upload(
                    image_file,
                    use_filename=True,
                    unique_filename=True,
                    tags=["trottinette"],
                    context={
                        "app": "trottinette_app"
                    }
                )
                data['image'] = result['secure_url']
            serializer = TrottineteSerializer(trottinette, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Trottinette.DoesNotExist:
            return Response({'error': 'Trottinette non trouvée'}, status=status.HTTP_404_NOT_FOUND)


class TrottinetteDeleteView(APIView):
    def delete(self, request, pk):
        try:
            trottinette = Trottinette.objects.get(pk=pk)
            Maintenance.objects.filter(Trottinette=trottinette).delete()
            TrottinetteBooking.objects.filter(Trottinette=trottinette).delete()
            trottinette.delete()
            return Response({'message': 'Trottinette supprimée'}, status=status.HTTP_200_OK)
        
        except Trottinette.DoesNotExist:
            return Response({'error': 'Trottinette introuvable'}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            print("ERREUR DELETE:", str(e))  # ← visible dans le terminal Django
            import traceback
            traceback.print_exc()           # ← affiche la stack trace complète
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class TrottinetteAvailableView(APIView):
    def get(self, request):
        trottinettes = Trottinette.objects.filter(status='disponible', battery__gt=20)
        serializer = TrottineteSerializer(trottinettes, many=True)
        return Response(serializer.data)


class TrottinetteNearbyView(APIView):
    def get(self, request):
        lat = request.query_params.get('lat')
        lng = request.query_params.get('lng')

        if not lat or not lng:
            return Response({'error': 'latitude et longitude requises'}, status=status.HTTP_400_BAD_REQUEST)

        trottinettes = Trottinette.objects.filter(status='disponible', battery__gt=20)[:20]
        serializer = TrottineteSerializer(trottinettes, many=True)
        return Response(serializer.data)

class MaintenanceAddView(APIView):
    def post(self, request):
        serializer = MaintenanceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MaintenanceListView(APIView):
    def get(self, request):
        maintenances = Maintenance.objects.all()
        serializer = MaintenanceSerializer(maintenances, many=True)
        return Response(serializer.data)


class MaintenanceByTrottinetteView(APIView):
    def get(self, request, trottinette_id):
        maintenances = Maintenance.objects.filter(Trottinette=trottinette_id)
        serializer = MaintenanceSerializer(maintenances, many=True)
        return Response(serializer.data)

class TrottinetteBookingAddView(APIView):
    def post(self, request):
        # Validate required fields
        trottinette_id = request.data.get('Trottinette')
        user_id = request.data.get('user')
        start_time = request.data.get('start_time')
        
        # Check if all required fields are provided
        if not trottinette_id:
            return Response({'error': 'Trottinette ID est requis'}, status=status.HTTP_400_BAD_REQUEST)
        if not user_id:
            return Response({'error': 'User ID est requis'}, status=status.HTTP_400_BAD_REQUEST)
        if not start_time:
            return Response({'error': 'Start time est requis'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            trottinette = Trottinette.objects.get(id=trottinette_id)
            user = User.objects.get(id=user_id)
            
            # Use serializer for validation
            booking_data = {
                'Trottinette': trottinette_id,
                'user': user_id,
                'start_time': start_time
            }
            serializer = TrottinetteBookingSerializer(data=booking_data)
            
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            # Validate trottinette availability
            if trottinette.status != 'disponible':
                return Response({'error': f'Trottinette non disponible. État actuel: {trottinette.status}'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Validate battery level
            if trottinette.battery <= 20:
                return Response({'error': f'Batterie insuffisante: {trottinette.battery}%'}, status=status.HTTP_400_BAD_REQUEST)

            booking = serializer.save()
            trottinette.status = 'réservée'
            trottinette.save()

            return Response(TrottinetteBookingSerializer(booking).data, status=status.HTTP_201_CREATED)

        except Trottinette.DoesNotExist:
            return Response({'error': 'Trottinette non trouvée'}, status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response({'error': 'Utilisateur non trouvé'}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            return Response({'error': f'Erreur de validation: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'Erreur lors de la création de la réservation: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TrottinetteBookingEndView(APIView):
    def get(self, request, booking_id):
        # Validate booking_id
        if not booking_id:
            return Response({'error': 'Booking ID est requis'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            booking = TrottinetteBooking.objects.get(id=booking_id)
            
            # Validate booking has start_time
            if not booking.start_time:
                return Response({'error': 'La réservation n\'a pas de début enregistré'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Validate booking is not already ended
            if booking.end_time:
                return Response({'error': 'La réservation est déjà terminée'}, status=status.HTTP_400_BAD_REQUEST)
            
            booking.end_time = timezone.now()
            duration = (booking.end_time - booking.start_time).total_seconds() / 60
            
            
            if duration < 0:
                return Response({'error': 'Temps de réservation invalide'}, status=status.HTTP_400_BAD_REQUEST)
            
            booking.total_cost = duration * booking.Trottinette.price_per_minute
            
            
            serializer = TrottinetteBookingSerializer(booking, data={
                'Trottinette': booking.Trottinette.id,
                'user': booking.user.id,
                'start_time': booking.start_time,
                'end_time': booking.end_time,
                'total_cost': booking.total_cost
            }, partial=True)
            
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()

            trottinette = booking.Trottinette
            trottinette.status = 'disponible'
            trottinette.save()

            return Response(TrottinetteBookingSerializer(booking).data)

        except TrottinetteBooking.DoesNotExist:
            return Response({'error': 'Réservation non trouvée'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'Erreur lors de la fin de la réservation: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserBookingsView(APIView):
    def get(self, request, user_id):
        bookings = TrottinetteBooking.objects.filter(user_id=user_id)
        serializer = TrottinetteBookingSerializer(bookings, many=True)
        return Response(serializer.data)


class TrottinetteBookingListView(APIView):
    def get(self, request):
        bookings = TrottinetteBooking.objects.all()
        serializer = TrottinetteBookingSerializer(bookings, many=True)
        return Response(serializer.data)

class TrottinetteBookingList(APIView):
    def get(self, request):
        bookings = TrottinetteBooking.objects.all()
        serializer = TrottinetteBookingSerializer(bookings, many=True)
        return Response(serializer.data)


class TrottinetteStatsView(APIView):
    def get(self, request):
        total = Trottinette.objects.count()
        disponible = Trottinette.objects.filter(status='disponible').count()
        reservee = Trottinette.objects.filter(status='réservée').count()
        en_cours = Trottinette.objects.filter(status='en_cours').count()
        maintenance = Trottinette.objects.filter(status='maintenance').count()

        return Response({
            'total': total,
            'disponible': disponible,
            'réservée': reservee,
            'en_cours': en_cours,
            'maintenance': maintenance,
        })
class TrottinetteBookingUpdate(APIView):
    def put(self, request, pk):
        try:
            booking = TrottinetteBooking.objects.get(id=pk)
            serializer = TrottinetteBookingSerializer(booking, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except TrottinetteBooking.DoesNotExist:
            return Response({'error': 'Réservation non trouvée'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'Erreur lors de la mise à jour de la réservation: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def patch(self, request, pk):   
        try:
            booking = TrottinetteBooking.objects.get(id=pk)
            serializer = TrottinetteBookingSerializer(booking, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except TrottinetteBooking.DoesNotExist:
            return Response({'error': 'Réservation non trouvée'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'Erreur lors de la mise à jour de la réservation: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class BookingConfirmView(APIView):
    def patch(self, request, pk):
        try:
            booking = TrottinetteBooking.objects.get(id=pk)

            if booking.status != 'en_attente':
                return Response({'error': f'Réservation déjà {booking.status}'}, status=status.HTTP_400_BAD_REQUEST)

            booking.status = 'confirmée'  # ← juste changer le statut
            booking.save()

            return Response({
                'message': 'Réservation confirmée',
                'booking': TrottinetteBookingSerializer(booking).data
            }, status=status.HTTP_200_OK)

        except TrottinetteBooking.DoesNotExist:
            return Response({'error': 'Réservation introuvable'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BookingRefuserView(APIView):
    def patch(self, request, booking_id):
        try:
            booking = TrottinetteBooking.objects.get(id=booking_id)

            if booking.status != 'en_attente':
                return Response({'error': f'Réservation déjà {booking.status}'}, status=status.HTTP_400_BAD_REQUEST)

            booking.status = 'refusée'  # ← juste changer le statut
            booking.Trottinette.status = 'disponible'
            booking.Trottinette.save()
            booking.save()

            return Response({
                'message': 'Réservation refusée',
                'booking': TrottinetteBookingSerializer(booking).data
            }, status=status.HTTP_200_OK)

        except TrottinetteBooking.DoesNotExist:
            return Response({'error': 'Réservation introuvable'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)