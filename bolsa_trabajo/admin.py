from django.contrib import admin
from .models import Postulacion,  OportunidadTrabajo

@admin.register(Postulacion)
class PostulacionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'correo', 'telefono', 'cv', 'mensaje', 'creado')
    list_filter = ('creado',)
    search_fields = ('nombre', 'correo')
    ordering = ('-creado',)
    actions = ['enviar_correo_notificacion']

    def enviar_correo_notificacion(self, request, queryset):
        for postulacion in queryset:
            # Aquí puedes usar la lógica para enviar el correo de notificación
            # por ejemplo, usando el módulo send_mail de Django
            from django.core.mail import send_mail
            send_mail(
                'Nueva Postulación Recibida',
                f'Hola {postulacion.nombre}, hemos recibido tu postulación.',
                'admin@vicafpro.com',
                [postulacion.correo]
            )
        self.message_user(request, "Notificaciones enviadas exitosamente.")
    enviar_correo_notificacion.short_description = 'Enviar notificación por correo'
    
@admin.register(OportunidadTrabajo)
class OportunidadTrabajoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'activo', 'estado', 'creado')
    list_filter = ('estado', 'activo')
    search_fields = ('titulo',)
    ordering = ('-creado',)
