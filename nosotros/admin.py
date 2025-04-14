from django.contrib import admin
from .models import Nosotros

@admin.register(Nosotros)
class NosotrosAdmin(admin.ModelAdmin):
    list_display = ('titulo',)
    search_fields = ('titulo', 'contenido')
