from django.db import models

class Trabajador(models.Model):
    nombre = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100)
    foto = models.ImageField(upload_to='trabajadores_fotos/')
    email = models.EmailField(unique=True)
    linkedin = models.URLField(blank=True)
    
    orden = models.PositiveIntegerField(
        default=0, 
        help_text="Posición en la web"
    )

    class Meta:
        ordering = ['orden', 'nombre']
        verbose_name = "Trabajador"
        verbose_name = "Trabajadores"

    def __str__(self):
        return f"[{self.orden}] {self.nombre} - {self.cargo}"