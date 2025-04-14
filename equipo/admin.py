from django.contrib import admin
from .models import MiembroEquipo

@admin.register(MiembroEquipo)
class MiembroEquipoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cargo', 'correo', 'linkedin')
    search_fields = ('nombre', 'cargo', 'correo')
