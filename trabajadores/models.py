from django.db import models

# Create your models here.
class Trabajador(models.Model):
    nombre = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100)
    foto = models.ImageField(upload_to='trabajadores_fotos/')
    email = models.EmailField(unique=True)
    linkedin = models.URLField(blank=True)

    def __str__(self):
        return f"{self.nombre} - {self.cargo}"