# servicios/api_views.py
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import Cotizacion, CotizacionDetalle, Servicio, DetalleServicio
from .serializers import CotizacionSerializer

class CotizacionViewSet(mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    """
    ViewSet para la creación, listado y detalle de cotizaciones.
    """
    queryset = Cotizacion.objects.all()
    serializer_class = CotizacionSerializer
    permission_classes = [IsAuthenticated]

    # No es necesario sobrescribir el método create si el serializador maneja los detalles.
    # El router de DRF ya mapea el método POST a esta acción.
    
    @action(detail=False, methods=['get'])
    def buscar_cliente(self, request):
        """
        Busca clientes por RUC o razón social.
        """
        query = request.GET.get('q', '')
        if not query:
            return Response([])
        
        try:
            cliente = ClienteProfile.objects.get(Q(ruc=query) | Q(razon_social__icontains=query))
            data = {
                'razon_social': cliente.razon_social,
                'persona_contacto': cliente.persona_contacto,
                'correo_contacto': cliente.correo_contacto,
                'telefono_contacto': cliente.telefono_contacto,
            }
            return Response(data)
        except ClienteProfile.DoesNotExist:
            return Response({'error': 'Cliente no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'])
    def buscar_servicio(self, request):
        """
        Busca servicios y sus detalles por nombre.
        """
        query = request.GET.get('q', '')
        if not query:
            return Response([])
        
        detalles_servicio = DetalleServicio.objects.filter(titulo__icontains=query).select_related('servicio')
        
        # Mapear los resultados a un formato JSON
        resultados = []
        for detalle in detalles_servicio:
            resultados.append({
                'servicio_id': detalle.servicio.id,
                'servicio_nombre': detalle.servicio.nombre,
                'detalle_id': detalle.id,
                'detalle_titulo': detalle.titulo,
                'normas': list(detalle.servicio.normas.values_list('nombre', flat=True)),
                'metodos': list(detalle.servicio.metodos.values_list('nombre', flat=True)),
            })
        
        return Response(resultados)