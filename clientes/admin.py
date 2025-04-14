from django.contrib import admin
from .models import Cliente

class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'logo', 'enlace')
    search_fields = ('nombre',)
    list_filter = ('enlace',)
    list_per_page = 10

admin.site.register(Cliente, ClienteAdmin)
