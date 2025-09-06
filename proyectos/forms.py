# proyectos/forms.py
from django import forms
from .models import (Proyecto,  OrdenDeEnsayo,
    Muestra,
    ResultadoEnsayo,
    DocumentoFinal)
from clientes.models import ClienteProfile
from trabajadores.models import TrabajadorProfile
from servicios.models import Cotizacion

class ProyectoForm(forms.ModelForm):
    """
    Formulario para la creación de un nuevo proyecto.
    """
    class Meta:
        model = Proyecto
        fields = [
            'cliente',
            'cotizacion',
            'servicios_usados',
            'nombre_proyecto',
            'descripcion_proyecto',
            'latitud',
            'longitud',
            'estado',
            'fecha_inicio',
            'fecha_fin_estimada',
        ]
        widgets = {
            'cliente': forms.Select(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-blue-950'}),
            'cotizacion': forms.Select(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-blue-950'}),
            'servicios_usados': forms.SelectMultiple(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-blue-950 h-32'}),
            'nombre_proyecto': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-blue-950'}),
            'descripcion_proyecto': forms.Textarea(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-blue-950'}),
            'latitud': forms.NumberInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-blue-950'}),
            'longitud': forms.NumberInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-blue-950'}),
            'estado': forms.Select(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-blue-950'}),
            'fecha_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-blue-950'}),
            'fecha_fin_estimada': forms.DateInput(attrs={'type': 'date', 'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-blue-950'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 bg-gray-700 text-white border-gray-600'})

        self.fields['cliente'].widget.attrs.update({'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 bg-gray-700 text-white border-gray-600'})
        self.fields['cotizacion'].widget.attrs.update({'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 bg-gray-700 text-white border-gray-600'})
        self.fields['servicios_usados'].widget.attrs.update({'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 bg-gray-700 text-white border-gray-600'})
        self.fields['estado'].widget.attrs.update({'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 bg-gray-700 text-white border-gray-600'})

class OrdenDeEnsayoForm(forms.ModelForm):
    """
    Formulario para crear y actualizar una Orden de Ensayo.
    """
    proyecto = forms.ModelChoiceField(
        queryset=Proyecto.objects.all(),
        label="Proyecto",
        required=True
    )
    supervisor_asignado = forms.ModelChoiceField(
        queryset=TrabajadorProfile.objects.filter(role='Supervisor'),
        label="Supervisor Asignado",
        required=False
    )

    class Meta:
        model = OrdenDeEnsayo
        fields = [
            'proyecto', 'codigo_orden', 'tipo_ensayo', 'norma_ensayo',
            'supervisor_asignado', 'fecha_entrega_programada', 'fecha_entrega_real',
            'estado_avance'
        ]
        widgets = {
            'proyecto': forms.Select(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-blue-900'}),
            'codigo_orden': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-blue-950'}),
            'tipo_ensayo': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-blue-950'}),
            'norma_ensayo': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-blue-950'}),
            'supervisor_asignado': forms.Select(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-blue-950'}),
            'fecha_entrega_programada': forms.DateInput(attrs={'type': 'date', 'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-blue-950'}),
            'fecha_entrega_real': forms.DateInput(attrs={'type': 'date', 'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-blue-950'}),
            'estado_avance': forms.Select(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-blue-950'}),
        }

class MuestraForm(forms.ModelForm):
    """
    Formulario para crear y actualizar una Muestra.
    """
    orden = forms.ModelChoiceField(
        queryset=OrdenDeEnsayo.objects.all(),
        label="Orden de Ensayo",
        required=True
    )

    class Meta:
        model = Muestra
        fields = [
            'orden', 'codigo_muestra', 'descripcion_muestra', 'id_lab',
            'tipo_muestra', 'masa_aprox_kg', 'fecha_recepcion',
            'fecha_fabricacion', 'fecha_ensayo_rotura', 'informe',
            'fecha_informe', 'estado', 'ensayos_a_realizar'
        ]
        widgets = {
            'orden': forms.Select(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-blue-950'}),
            'codigo_muestra': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-blue-950'}),
            'descripcion_muestra': forms.Textarea(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-blue-950'}),
            'id_lab': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-blue-950'}),
            'tipo_muestra': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-blue-950'}),
            'masa_aprox_kg': forms.NumberInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-blue-950'}),
            'fecha_recepcion': forms.DateInput(attrs={'type': 'date', 'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-blue-950'}),
            'fecha_fabricacion': forms.DateInput(attrs={'type': 'date', 'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-blue-950'}),
            'fecha_ensayo_rotura': forms.DateInput(attrs={'type': 'date', 'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-blue-950'}),
            'informe': forms.Textarea(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-blue-950'}),
            'fecha_informe': forms.DateInput(attrs={'type': 'date', 'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-blue-950'}),
            'estado': forms.Select(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-blue-950'}),
            'ensayos_a_realizar': forms.Textarea(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-blue-950'}),
        }

class ResultadoEnsayoForm(forms.ModelForm):
    """
    Formulario para crear y actualizar un Resultado de Ensayo.
    """
    muestra = forms.ModelChoiceField(
        queryset=Muestra.objects.all(),
        label="Muestra",
        required=True
    )
    tecnico_asignado = forms.ModelChoiceField(
        queryset=TrabajadorProfile.objects.filter(role='Técnico'),
        label="Técnico Asignado",
        required=False
    )

    class Meta:
        model = ResultadoEnsayo
        fields = [
            'muestra', 'tecnico_asignado', 'resultados_json', 'observaciones',
            'fecha_realizacion'
        ]
        widgets = {
            'muestra': forms.Select(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-blue-950'}),
            'tecnico_asignado': forms.Select(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-blue-950'}),
            'resultados_json': forms.Textarea(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-blue-950', 'rows': 4}),
            'observaciones': forms.Textarea(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-blue-950', 'rows': 4}),
            'fecha_realizacion': forms.DateInput(attrs={'type': 'date', 'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-blue-950'}),
        }

class DocumentoFinalForm(forms.ModelForm):
    """
    Formulario para crear y actualizar un Documento Final.
    Se ha mejorado la estética con Tailwind CSS.
    """
    proyecto = forms.ModelChoiceField(
        queryset=Proyecto.objects.all(),
        label="Proyecto",
        required=True
    )

    class Meta:
        model = DocumentoFinal
        fields = [
            'proyecto', 'titulo', 'archivo_original', 'resumen_ejecutivo_ia',
            'analisis_detallado_ia', 'recomendaciones_ia', 'firma_supervisor',
            'firma_cliente', 'fecha_emision'
        ]
        widgets = {
            'proyecto': forms.Select(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-blue-950 shadow-sm'}),
            'titulo': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-blue-950 shadow-sm'}),
            'archivo_original': forms.FileInput(attrs={'class': 'w-full px-4 py-2 bg-blue-950 rounded-md shadow-sm'}),
            'resumen_ejecutivo_ia': forms.Textarea(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-blue-950 shadow-sm', 'rows': 4}),
            'analisis_detallado_ia': forms.Textarea(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-blue-950 shadow-sm', 'rows': 6}),
            'recomendaciones_ia': forms.Textarea(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-blue-950 shadow-sm', 'rows': 4}),
            'firma_supervisor': forms.FileInput(attrs={'class': 'w-full px-4 py-2 bg-blue-950 rounded-md shadow-sm'}),
            'firma_cliente': forms.FileInput(attrs={'class': 'w-full px-4 py-2 bg-blue-950 rounded-md shadow-sm'}),
            'fecha_emision': forms.DateInput(attrs={'type': 'date', 'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-blue-950  shadow-sm'}),
        }
