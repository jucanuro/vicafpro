from django import forms
from django.forms import inlineformset_factory
from .models import Cotizacion, CotizacionDetalle, Servicio, DetalleServicio
from clientes.models import ClienteProfile
from trabajadores.models import TrabajadorProfile

# Clases base de Tailwind CSS para consistencia visual
BASE_INPUT_CLASS = 'w-full p-3 rounded-lg bg-slate-700/50 text-slate-200 border border-slate-600 focus:outline-none focus:ring-2 focus:ring-emerald-500 transition-all duration-300'
BASE_TEXTAREA_CLASS = 'w-full p-3 rounded-lg bg-slate-700/50 text-slate-200 border border-slate-600 focus:outline-none focus:ring-2 focus:ring-emerald-500 transition-all duration-300 resize-y'
BASE_SELECT_CLASS = 'w-full p-3 rounded-lg bg-slate-700/50 text-slate-200 border border-slate-600 focus:outline-none focus:ring-2 focus:ring-emerald-500 transition-all duration-300'
FILE_INPUT_CLASS = 'w-full text-sm text-slate-300 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-emerald-500 file:text-white hover:file:bg-emerald-600 transition-colors duration-300'

class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = ['nombre', 'descripcion', 'imagen', 'orden']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': BASE_INPUT_CLASS}),
            'descripcion': forms.Textarea(attrs={'class': BASE_TEXTAREA_CLASS, 'rows': 4}),
            'orden': forms.NumberInput(attrs={'class': BASE_INPUT_CLASS}),
            'imagen': forms.ClearableFileInput(attrs={'class': FILE_INPUT_CLASS}),
        }

class DetalleServicioForm(forms.ModelForm):
    class Meta:
        model = DetalleServicio
        fields = ['servicio', 'titulo', 'descripcion', 'imagen']
        widgets = {
            'servicio': forms.Select(attrs={'class': BASE_SELECT_CLASS}),
            'titulo': forms.TextInput(attrs={'class': BASE_INPUT_CLASS}),
            'descripcion': forms.Textarea(attrs={'class': BASE_TEXTAREA_CLASS, 'rows': 4}),
            'imagen': forms.ClearableFileInput(attrs={'class': FILE_INPUT_CLASS}),
        }
        
class CotizacionForm(forms.ModelForm):
    class Meta:
        model = Cotizacion
        fields = [
            'cliente',
            'numero_oferta',
            'persona_contacto',
            'correo_contacto',
            'telefono_contacto',
            'estado',
            'plazo_entrega_dias',
            'forma_pago',
            'validez_oferta_dias',
            'monto_total',
        ]
        widgets = {
            'cliente': forms.Select(attrs={'class': BASE_SELECT_CLASS}),
            'numero_oferta': forms.TextInput(attrs={'class': BASE_INPUT_CLASS}),
            'persona_contacto': forms.TextInput(attrs={'class': BASE_INPUT_CLASS}),
            'correo_contacto': forms.EmailInput(attrs={'class': BASE_INPUT_CLASS}),
            'telefono_contacto': forms.TextInput(attrs={'class': BASE_INPUT_CLASS}),
            'estado': forms.Select(attrs={'class': BASE_SELECT_CLASS}),
            'plazo_entrega_dias': forms.NumberInput(attrs={'class': BASE_INPUT_CLASS}),
            'forma_pago': forms.Select(attrs={'class': BASE_SELECT_CLASS}),
            'validez_oferta_dias': forms.NumberInput(attrs={'class': BASE_INPUT_CLASS}),
            'monto_total': forms.NumberInput(attrs={'class': BASE_INPUT_CLASS}),
        }


