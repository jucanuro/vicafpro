from django.db import models

class Nosotros(models.Model):
    titulo = models.CharField(max_length=100)
    contenido = models.TextField()
    imagen = models.ImageField(upload_to='nosotros/', blank=True, null=True)

    def __str__(self):
        return self.titulo
