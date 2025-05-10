from django import forms
from .models import Postulacion

class PostulacionForm(forms.ModelForm):
    class Meta:
        model = Postulacion
        fields = ['nombre', 'correo', 'telefono', 'cv', 'mensaje']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'w-1/2 px-4 py-1 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm text-gray-800'
            }),
            'correo': forms.EmailInput(attrs={
                'class': 'w-1/2 px-4 py-1 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm text-gray-800'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'w-1/2 px-4 py-1 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm text-gray-800'
            }),
            'cv': forms.ClearableFileInput(attrs={
                'class': 'w-1/2 px-4 py-1 border border-gray-300 rounded-xl bg-white text-sm text-gray-800'
            }),
            'mensaje': forms.Textarea(attrs={
                'class': 'w-full px-4 py-1 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm text-gray-800',
                'rows': 4
            }),
        }

