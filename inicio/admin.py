from django.contrib import admin
from .models import CarruselInicio

@admin.register(CarruselInicio)
class CarruselInicioAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'descripcion', 'enlace')
    search_fields = ('titulo', 'descripcion')
