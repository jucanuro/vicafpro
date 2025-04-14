from django.contrib import admin
from .models import MensajeContacto

class MensajeContactoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'correo', 'asunto', 'creado')  # Mostrar columnas
    search_fields = ('nombre', 'correo', 'asunto')  # Búsqueda por estos campos
    list_filter = ('creado',)  # Filtrar por fecha de creación
    actions = ['enviar_correo']  # Añadir acción personalizada para enviar el correo

    def enviar_correo(self, request, queryset):
        for mensaje in queryset:
            mensaje.enviar_correo()  # Enviar el correo para cada mensaje
        self.message_user(request, "Correos enviados a los contactos seleccionados.")

    enviar_correo.short_description = "Enviar correos a los mensajes seleccionados"

admin.site.register(MensajeContacto, MensajeContactoAdmin)
