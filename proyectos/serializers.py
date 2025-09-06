# proyectos/serializers.py

from rest_framework import serializers
from .models import (
    Proyecto, 
    OrdenDeEnsayo, 
    Muestra, 
    ResultadoEnsayo, 
    DocumentoFinal, 
    Servicio
)

# ================================================================
# Serializadores para la aplicación Proyectos
# ================================================================

class ProyectoSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Proyecto.
    Utilizamos 'ModelSerializer' que simplifica la creación de serializers
    para modelos de Django.
    """
    class Meta:
        model = Proyecto
        # Incluye todos los campos del modelo en el serializador.
        fields = '__all__'

class OrdenDeEnsayoSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo OrdenDeEnsayo.
    """
    class Meta:
        model = OrdenDeEnsayo
        fields = '__all__'

class MuestraSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Muestra.
    """
    class Meta:
        model = Muestra
        fields = '__all__'

class ResultadoEnsayoSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo ResultadoEnsayo.
    """
    class Meta:
        model = ResultadoEnsayo
        fields = '__all__'

class DocumentoFinalSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo DocumentoFinal.
    """
    class Meta:
        model = DocumentoFinal
        fields = '__all__'

class ServicioSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Servicio.
    """
    class Meta:
        model = Servicio
        fields = '__all__'

