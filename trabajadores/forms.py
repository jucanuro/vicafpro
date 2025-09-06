from django import forms
from .models import TrabajadorProfile

class TrabajadorProfileForm(forms.ModelForm):
    class Meta:
        model = TrabajadorProfile
        # Incluye los campos que quieres que los usuarios puedan modificar.
        # Excluye los campos automáticos como `creado_en` y `actualizado_en`.
        fields = [
            'user', 
            'nombre_completo', 
            'role', 
            'foto', 
            'linkedin', 
            'firma_electronica'
        ]