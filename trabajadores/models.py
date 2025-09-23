# trabajadores/models.py

from django.db import models
from django.conf import settings
from django.utils import timezone

class TrabajadorProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    ROLES = [
        ('ADMINISTRADOR', 'Administrador'),
        ('SUPERVISOR', 'Supervisor de Laboratorio'),
        ('TECNICO', 'Técnico de Laboratorio'),
    ]

    nombre_completo = models.CharField(max_length=255, verbose_name="Nombre Completo")
    role = models.CharField(max_length=20, choices=ROLES, default='TECNICO', verbose_name="Rol")
    foto = models.ImageField(upload_to='trabajadores_fotos/', blank=True, null=True, verbose_name="Foto")
    linkedin = models.URLField(blank=True, null=True, verbose_name="Perfil de LinkedIn")
    firma_electronica = models.ImageField(upload_to='firmas/', blank=True, null=True, verbose_name="Firma Electrónica")

    creado_en = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    actualizado_en = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")

    def __str__(self):
        return f"{self.nombre_completo} ({self.get_role_display()})"

    class Meta:
        verbose_name = "Perfil de Trabajador"
        verbose_name_plural = "Perfiles de Trabajadores"
        ordering = ['nombre_completo']