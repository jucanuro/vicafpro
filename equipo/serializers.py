from rest_framework import serializers
from .models import MiembroEquipo

class MiembroEquipoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MiembroEquipo
        fields = '__all__'
