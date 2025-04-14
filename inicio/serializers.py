from rest_framework import serializers
from .models import CarruselInicio

class CarruselInicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarruselInicio
        fields = '__all__'
