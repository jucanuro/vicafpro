from rest_framework import generics
from .models import CarruselInicio
from .serializers import CarruselInicioSerializer

class CarruselInicioListCreateView(generics.ListCreateAPIView):
    queryset = CarruselInicio.objects.all()
    serializer_class = CarruselInicioSerializer

class CarruselInicioRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CarruselInicio.objects.all()
    serializer_class = CarruselInicioSerializer
