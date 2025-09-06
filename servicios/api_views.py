# servicios/api_views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Cotizacion
from .serializers import CotizacionSerializer

class CotizacionViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite ver o editar cotizaciones.
    """
    queryset = Cotizacion.objects.all().order_by('-fecha_creacion')
    serializer_class = CotizacionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(creado_por=self.request.user.trabajadorprofile)