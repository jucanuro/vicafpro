from rest_framework import serializers
from .models import ClienteProfile

class ClienteProfileSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = ClienteProfile
        fields = [
            'id', 
            'razon_social', 
            'ruc', 
            'direccion',
            'persona_contacto', 
            'cargo_contacto', 
            'celular_contacto', 
            'correo_contacto',
            'firma_electronica', 
            'creado_en', 
            'actualizado_en'
        ]