from django.contrib import admin
from .models import Servicio, DetalleServicio

class DetalleServicioInline(admin.TabularInline):
    model = DetalleServicio
    extra = 1

@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'orden')
    search_fields = ('nombre',)
    inlines = [DetalleServicioInline]

@admin.register(DetalleServicio)
class DetalleServicioAdmin(admin.ModelAdmin):
    list_display = ('servicio', 'titulo')
    search_fields = ('titulo', 'servicio__nombre')
