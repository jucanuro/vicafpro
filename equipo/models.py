from django.db import models

class MiembroEquipo(models.Model):
    nombre = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100)
    descripcion = models.TextField()
    foto = models.ImageField(upload_to='equipo/')
    linkedin = models.URLField(blank=True, null=True)
    correo = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.nombre
