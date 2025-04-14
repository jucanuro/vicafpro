from rest_framework import generics
from .models import MiembroEquipo
from .serializers import MiembroEquipoSerializer

class MiembroEquipoListCreateView(generics.ListCreateAPIView):
    queryset = MiembroEquipo.objects.all()
    serializer_class = MiembroEquipoSerializer

class MiembroEquipoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MiembroEquipo.objects.all()
    serializer_class = MiembroEquipoSerializer
