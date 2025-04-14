from rest_framework import generics
from .models import Servicio, DetalleServicio
from .serializers import ServicioSerializer, DetalleServicioSerializer

class ServicioListView(generics.ListCreateAPIView):
    queryset = Servicio.objects.all().order_by('orden')
    serializer_class = ServicioSerializer

class ServicioDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Servicio.objects.all()
    serializer_class = ServicioSerializer

class DetalleServicioListView(generics.ListCreateAPIView):
    queryset = DetalleServicio.objects.all()
    serializer_class = DetalleServicioSerializer

class DetalleServicioDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DetalleServicio.objects.all()
    serializer_class = DetalleServicioSerializer
