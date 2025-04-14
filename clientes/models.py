from django.db import models

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='clientes/')
    enlace = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.nombre
