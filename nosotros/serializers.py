from rest_framework import serializers
from .models import Nosotros

class NosotrosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nosotros
        fields = '__all__'
