from rest_framework import serializers
from .models import Servicio, DetalleServicio

class DetalleServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleServicio
        fields = '__all__'

class ServicioSerializer(serializers.ModelSerializer):
    detalles = DetalleServicioSerializer(many=True, read_only=True)

    class Meta:
        model = Servicio
        fields = '__all__'
