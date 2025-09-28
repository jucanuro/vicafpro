from django.contrib import admin
from .models import Proyecto, OrdenDeEnsayo, Muestra , DocumentoFinal, ResultadoEnsayo

# Registramos los modelos para que aparezcan en el panel de administración de Django.

from django.contrib import admin
from .models import Proyecto

@admin.register(Proyecto)
class ProyectoAdmin(admin.ModelAdmin):
    list_display = ('nombre_proyecto', 'cliente', 'cotizacion', 'estado', 'numero_muestras', 'numero_muestras_registradas', 'fecha_inicio', 'fecha_entrega_estimada')
    list_filter = ('estado', 'fecha_inicio', 'fecha_entrega_estimada')
    search_fields = ('nombre_proyecto', 'cliente__razon_social', 'cotizacion__numero_oferta')

@admin.register(OrdenDeEnsayo)
class OrdenDeEnsayoAdmin(admin.ModelAdmin):
    list_display = ('muestra', 'proyecto', 'tipo_ensayo', 'fecha_entrega_programada')
    list_filter = ('tipo_ensayo', 'fecha_entrega_programada')
    search_fields = ('muestra__codigo_muestra', 'proyecto__nombre_proyecto')
    
@admin.register(Muestra)
class MuestraAdmin(admin.ModelAdmin):
    list_display = ('codigo_muestra', 'proyecto', 'tipo_muestra', 'estado', 'fecha_recepcion')
    list_filter = ('estado', 'tipo_muestra', 'fecha_recepcion')
    search_fields = ('codigo_muestra', 'descripcion_muestra', 'proyecto__nombre_proyecto')
    
@admin.register(ResultadoEnsayo)
class ResultadoEnsayoAdmin(admin.ModelAdmin):
    list_display = ('muestra', 'tecnico_asignado', 'fecha_realizacion')
    list_filter = ('tecnico_asignado', 'fecha_realizacion')
    search_fields = ('muestra__codigo_muestra', 'tecnico_asignado__user__username')

@admin.register(DocumentoFinal)
class DocumentoFinalAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'proyecto', 'fecha_emision')
    list_filter = ('fecha_emision', 'proyecto__cliente')
    search_fields = ('titulo', 'proyecto__nombre_proyecto')