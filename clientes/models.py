from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone

class ClienteProfile(models.Model):
    """
    Modelo de perfil para extender el modelo de usuario de Django con información
    específica del cliente.
    """
    # Relación uno a uno con el modelo de usuario de Django.
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    # Información fiscal y de dirección
    razon_social = models.CharField(max_length=255, blank=True, null=True, verbose_name="Razón Social")
    ruc = models.CharField(max_length=11, unique=True, blank=True, null=True, verbose_name="RUC")
    direccion = models.CharField(max_length=255, blank=True, null=True, verbose_name="Dirección")

    # Información de contacto principal del cliente
    persona_contacto = models.CharField(max_length=255, blank=True, null=True, verbose_name="Persona de Contacto")
    cargo_contacto = models.CharField(max_length=100, blank=True, null=True, verbose_name="Cargo del Contacto")
    celular_contacto = models.CharField(max_length=20, blank=True, null=True, verbose_name="Celular del Contacto")
    correo_contacto = models.EmailField(max_length=255, blank=True, null=True, verbose_name="Correo Electrónico del Contacto")
        
    firma_electronica = models.ImageField(upload_to='firmas_clientes/', blank=True, null=True, verbose_name="Firma Electrónica")


    # Campos de trazabilidad automáticos
    creado_en = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    actualizado_en = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")

    def __str__(self):
        """
        Representación en string del objeto, útil para el panel de administración.
        """
        username = self.user.username if self.user else "Usuario Desconocido"
        return f"Perfil de {username} ({self.razon_social})"

    class Meta:
        verbose_name = "Perfil de Cliente"
        verbose_name_plural = "Perfiles de Clientes"
        ordering = ['razon_social']