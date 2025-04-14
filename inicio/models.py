from django.db import models

class CarruselInicio(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='inicio/')
    enlace = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.titulo

