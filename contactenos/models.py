from django.db import models
from django.core.mail import send_mail
from django.conf import settings

class MensajeContacto(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()
    asunto = models.CharField(max_length=150)
    mensaje = models.TextField()
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - {self.asunto}"

    def enviar_correo(self):
        send_mail(
            subject=f"Nuevo mensaje de contacto: {self.asunto}",
            message=self.mensaje,
            from_email=self.correo,
            recipient_list=[settings.CONTACT_EMAIL],
        )
