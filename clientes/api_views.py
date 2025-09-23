# api_views.py
from rest_framework import generics, serializers
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import ClienteProfile
from .serializers import ClienteProfileSerializer

class ClienteProfileListCreateAPIView(generics.ListCreateAPIView):
    """
    Maneja las peticiones GET (listar todos) y POST (crear nuevo).
    """
    queryset = ClienteProfile.objects.all()
    serializer_class = ClienteProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ClienteProfileDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Maneja las peticiones GET (obtener un cliente), PUT/PATCH (actualizar) y DELETE.
    """
    queryset = ClienteProfile.objects.all()
    serializer_class = ClienteProfileSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'