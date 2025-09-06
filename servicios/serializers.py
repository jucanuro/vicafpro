from rest_framework import serializers
from .models import Servicio, DetalleServicio,Cotizacion, CotizacionDetalle

class DetalleServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleServicio
        fields = '__all__'

class ServicioSerializer(serializers.ModelSerializer):
    detalles = DetalleServicioSerializer(many=True, read_only=True)
    class Meta:
        model = Servicio
        fields = '__all__'

class CotizacionDetalleSerializer(serializers.ModelSerializer):
    # Campos de solo lectura para mostrar el nombre del servicio y detalle
    servicio_nombre = serializers.CharField(source='servicio.nombre', read_only=True)
    detalle_servicio_titulo = serializers.CharField(source='detalle_servicio.titulo', read_only=True)
    
    class Meta:
        model = CotizacionDetalle
        fields = ['servicio', 'detalle_servicio', 'cantidad', 'precio_unitario', 'subtotal', 'servicio_nombre', 'detalle_servicio_titulo']
        read_only_fields = ['subtotal']

class CotizacionSerializer(serializers.ModelSerializer):
    # Campo para los detalles de la cotización, usando el serializador anidado
    detalles_cotizacion = CotizacionDetalleSerializer(many=True)

    class Meta:
        model = Cotizacion
        fields = [
            'numero_oferta', 
            'fecha_creacion', 
            'cliente',  
            'persona_contacto', 
            'correo_contacto', 
            'telefono_contacto', 
            'forma_pago', 
            'validez_oferta_dias', 
            'plazo_entrega_dias', 
            'estado', 
            'monto_total', 
            'detalles_cotizacion', # <-- Incluye el serializador anidado aquí
        ]
        read_only_fields = ['monto_total', 'creado_por']

    def create(self, validated_data):
        detalles_data = validated_data.pop('detalles_cotizacion')
        cotizacion = Cotizacion.objects.create(**validated_data)
        
        for detalle_data in detalles_data:
            CotizacionDetalle.objects.create(cotizacion=cotizacion, **detalle_data)
        
        return cotizacion

    def update(self, instance, validated_data):
        detalles_data = validated_data.pop('detalles_cotizacion')
        # ... lógica de actualización para la cotización y sus detalles
        return instance
