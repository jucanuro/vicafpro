# servicios/forms.py
from django import forms
from django.forms import inlineformset_factory
from .models import Cotizacion, CotizacionDetalle,Servicio, DetalleServicio
from clientes.models import ClienteProfile
from trabajadores.models import TrabajadorProfile

class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = ['nombre', 'descripcion', 'imagen', 'orden']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-input bg-slate-800 rounded-lg border border-slate-400 p-2'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-textarea bg-slate-800 px-1 rounded-lg shadow-lg mt-2 border border-slate-400'}),
            'orden': forms.NumberInput(attrs={'class': 'form-input bg-slate-800 px-2 rounded-lg border border-slate-400 p-2'}),
        }

class DetalleServicioForm(forms.ModelForm):
    class Meta:
        model = DetalleServicio
        fields = ['servicio', 'titulo', 'descripcion', 'imagen']
        widgets = {
            'servicio': forms.Select(attrs={'class': 'form-select'}),
            'titulo': forms.TextInput(attrs={'class': 'form-input bg-slate-800 rounded-lg border border-slate-400 p-2'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-textarea bg-slate-800 rounded-lg border border-slate-400 p-2'}),
        }
        
class CotizacionForm(forms.ModelForm):
    class Meta:
        model = Cotizacion
        # Incluye solo los campos que existen en el modelo Cotizacion
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
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'numero_oferta': forms.TextInput(attrs={'class': 'form-control'}),
            'persona_contacto': forms.TextInput(attrs={'class': 'form-control'}),
            'correo_contacto': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono_contacto': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'plazo_entrega_dias': forms.NumberInput(attrs={'class': 'form-control'}),
            'forma_pago': forms.Select(attrs={'class': 'form-control'}),
            'validez_oferta_dias': forms.NumberInput(attrs={'class': 'form-control'}),
            'monto_total': forms.NumberInput(attrs={'class': 'form-control'}),
        }

# ================================================================
# Formulario para el modelo CotizacionDetalle (antes CotizacionItem)
# ================================================================
class CotizacionDetalleForm(forms.ModelForm):
    class Meta:
        model = CotizacionDetalle
        # Incluye solo los campos que existen en el modelo CotizacionDetalle
        fields = [
            'servicio',
            'detalle_servicio',
            'und',
            'cantidad',
            'precio_unitario'
        ]
        widgets = {
            'servicio': forms.Select(attrs={'class': 'form-control'}),
            'detalle_servicio': forms.Select(attrs={'class': 'form-control'}),
            'und': forms.TextInput(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control'}),
        }
  
        
CotizacionDetalleFormSet = inlineformset_factory(
    Cotizacion,
    CotizacionDetalle,
    form=CotizacionDetalleForm,
    extra=1, # Número de formularios vacíos por defecto
    can_delete=True
)