from django import forms
from .models import ClienteProfile # Asume que tu modelo está en la misma app

class ClienteProfileForm(forms.ModelForm):
    """
    Formulario para el modelo ClienteProfile, con estilos de Tailwind CSS.
    """
    class Meta:
        model = ClienteProfile
        fields = [
            'razon_social',
            'ruc',
            'direccion',
            'persona_contacto',
            'cargo_contacto',
            'celular_contacto',
            'correo_contacto',
            'firma_electronica',
        ]
        
        # Define una clase base para todos los campos de texto
        base_class = 'w-full p-3 rounded-lg bg-slate-700/50 text-slate-200 border border-slate-600 focus:outline-none focus:ring-2 focus:ring-emerald-500 transition-all duration-300'
        
        widgets = {
            'razon_social': forms.TextInput(attrs={'class': base_class}),
            'ruc': forms.TextInput(attrs={'class': base_class}),
            'direccion': forms.TextInput(attrs={'class': base_class}),
            'persona_contacto': forms.TextInput(attrs={'class': base_class}),
            'cargo_contacto': forms.TextInput(attrs={'class': base_class}),
            'celular_contacto': forms.TextInput(attrs={'class': base_class}),
            'correo_contacto': forms.EmailInput(attrs={'class': base_class}),
            'firma_electronica': forms.ClearableFileInput(attrs={'class': 'w-full text-sm text-slate-300 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-emerald-500 file:text-white hover:file:bg-emerald-600 transition-colors duration-300'}),
        }
        
        labels = {
            'razon_social': 'Razón Social',
            'ruc': 'RUC',
            'direccion': 'Dirección',
            'persona_contacto': 'Persona de Contacto',
            'cargo_contacto': 'Cargo del Contacto',
            'celular_contacto': 'Celular del Contacto',
            'correo_contacto': 'Correo Electrónico del Contacto',
            'firma_electronica': 'Firma Electrónica',
        }
