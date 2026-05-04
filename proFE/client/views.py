from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password, make_password
from .models import Client
from .serializers import ClientSerializer, ClientRegistrationSerializer

class ClientCreateView(APIView):
    def post(self, request):
        try:
            # Copy data — request.data is immutable
            data = request.data.copy()

            # Hash password before passing to serializer
            if 'password' in data:
                data['password'] = make_password(data['password'])

            serializer = ClientSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                return Response({
                    'message': 'Client created successfully',
                    'client': serializer.data
                }, status=status.HTTP_201_CREATED)

            return Response({
                'error': 'Validation failed',
                'details': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                'error': f'Error creating client: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ClientListView(APIView):
    def get(self, request):
        clients = Client.objects.all()
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data)


class ClientRegistrationView(APIView):
    def post(self, request):
        serializer = ClientRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            client = serializer.save()
            return Response({
                'message': 'Client registered successfully',
                'client': ClientSerializer(client).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClientLoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        if not email or not password:
            return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            client = Client.objects.get(email=email)
        except Client.DoesNotExist:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
        if check_password(password, client.password):
            serializer = ClientSerializer(client)
            return Response({
                'message': 'Login successful',
                'client': serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
class ClientDeleteView(APIView):
    def delete(self, request, client_id):
        try:
            client = Client.objects.get(id=client_id)
            client.delete()
            return Response({
                'message': 'Client deleted successfully'
            }, status=status.HTTP_200_OK)

        except Client.DoesNotExist:
            return Response({
                'error': 'Client not found'
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({
                'error': f'Error deleting client: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ClientDetailView(APIView):
    def get(self, request, client_id):
        try:
            client = Client.objects.get(id=client_id)
            serializer = ClientSerializer(client)
            return Response(serializer.data)
        except Client.DoesNotExist:
            return Response({'error': 'Client not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, client_id): 
        try:
            client = Client.objects.get(id=client_id)
            client.delete()
            return Response({'message': 'Client deleted successfully'}, status=status.HTTP_200_OK)
        except Client.DoesNotExist:
            return Response({'error': 'Client not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'Error deleting client: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
# Create your views here.
