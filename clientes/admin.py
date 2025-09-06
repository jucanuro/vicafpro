# clientes/admin.py

from django.contrib import admin
from .models import ClienteProfile # Importamos ClienteProfile

# class ClienteProfileAdmin(admin.ModelAdmin):
#     list_display = ('user', 'razon_social', 'ruc', 'telefono')
#     search_fields = ('user__username', 'razon_social', 'ruc')
#     raw_id_fields = ('user',) # Útil si tienes muchos usuarios para no cargar la lista completa

# Registra tu modelo ClienteProfile
# admin.site.register(ClienteProfile, ClienteProfileAdmin) # Si usas la clase Admin personalizada
admin.site.register(ClienteProfile) # Si no necesitas una personalización por ahora