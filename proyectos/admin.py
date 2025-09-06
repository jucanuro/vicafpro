from django.contrib import admin
from .models import Proyecto, OrdenDeEnsayo, Muestra, ResultadoEnsayo, DocumentoFinal

# Registramos los modelos para que aparezcan en el panel de administración de Django.

@admin.register(Proyecto)
class ProyectoAdmin(admin.ModelAdmin):
    list_display = ('nombre_proyecto', 'cliente', 'estado', 'fecha_inicio', 'fecha_finalizacion_real', 'actualizado_en')
    list_filter = ('estado', 'fecha_inicio', 'cliente')
    search_fields = ('nombre_proyecto', 'descripcion_proyecto', 'cliente__razon_social')
    date_hierarchy = 'creado_en'

@admin.register(OrdenDeEnsayo)
class OrdenDeEnsayoAdmin(admin.ModelAdmin):
    list_display = ('codigo_orden', 'proyecto', 'tipo_ensayo', 'estado_avance', 'supervisor_asignado', 'fecha_entrega_programada')
    list_filter = ('estado_avance', 'supervisor_asignado', 'fecha_entrega_programada')
    search_fields = ('codigo_orden', 'tipo_ensayo', 'proyecto__nombre_proyecto')

@admin.register(Muestra)
class MuestraAdmin(admin.ModelAdmin):
    list_display = ('codigo_muestra', 'orden')
    search_fields = ('codigo_muestra', 'descripcion_muestra', 'orden__codigo_orden')

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