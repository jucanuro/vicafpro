# servicios/serializers.py
from rest_framework import serializers
from .models import Cotizacion, CotizacionDetalle, Servicio, DetalleServicio
from clientes.models import ClienteProfile
from decimal import Decimal

# Serializador para los detalles de la cotización
class CotizacionDetalleSerializer(serializers.ModelSerializer):
    servicio = serializers.PrimaryKeyRelatedField(queryset=Servicio.objects.all())
    detalle_servicio = serializers.PrimaryKeyRelatedField(queryset=DetalleServicio.objects.all())

    class Meta:
        model = CotizacionDetalle
        fields = ['servicio', 'detalle_servicio', 'und', 'cantidad', 'precio_unitario']

# Serializador principal para la cotización
class CotizacionSerializer(serializers.ModelSerializer):
    # Añadimos los campos del cliente para poder recibirlos en la petición
    # NO son campos del modelo Cotizacion, por lo que deben ser 'writable'
    # y gestionados en el método create del serializador.
    ruc = serializers.CharField(write_only=True)
    razon_social = serializers.CharField(write_only=True)
    detalles_cotizacion = CotizacionDetalleSerializer(many=True)

    class Meta:
        model = Cotizacion
        fields = [
            'numero_oferta', 
            'ruc',
            'razon_social',
            'persona_contacto', 
            'correo_contacto', 
            'telefono_contacto',
            'forma_pago',
            'validez_oferta_dias',
            'plazo_entrega_dias',
            'monto_total',
            'detalles_cotizacion',
        ]
        read_only_fields = ['monto_total', 'numero_oferta']

    def create(self, validated_data):
        # 1. Extraer los datos de detalles y cliente
        detalles_data = validated_data.pop('detalles_cotizacion')
        ruc = validated_data.pop('ruc')
        razon_social = validated_data.pop('razon_social')
        
        # 2. Buscar o crear el cliente usando el RUC
        cliente_data = {
            'razon_social': razon_social,
            'persona_contacto': validated_data.get('persona_contacto'),
            'correo_contacto': validated_data.get('correo_contacto'),
            'telefono_contacto': validated_data.get('telefono_contacto'),
        }
        
        cliente, created = ClienteProfile.objects.update_or_create(
            ruc=ruc, 
            defaults=cliente_data
        )
        
        # 3. Crear la instancia de la cotización
        cotizacion = Cotizacion.objects.create(cliente=cliente, **validated_data)
        
        # 4. Crear los detalles de la cotización
        for detalle_data in detalles_data:
            CotizacionDetalle.objects.create(cotizacion=cotizacion, **detalle_data)
        
        return cotizacion

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Añadir los campos del cliente para la respuesta de la API
        representation['razon_social'] = instance.cliente.razon_social
        representation['ruc'] = instance.cliente.ruc
        return representation