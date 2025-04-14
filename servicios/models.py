from django.db import models

class Servicio(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='servicios/')
    orden = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.nombre

class DetalleServicio(models.Model):
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, related_name='detalles')
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='servicios/detalles/', blank=True, null=True)

    def __str__(self):
        return f"{self.servicio.nombre} - {self.titulo}"
