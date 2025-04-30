from django.db import models

class Postulacion(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()
    telefono = models.CharField(max_length=20, blank=True, null=True)
    cv = models.FileField(upload_to='bolsa_trabajo/cv/')
    mensaje = models.TextField(blank=True, null=True)
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - {self.correo}"
    

class OportunidadTrabajo(models.Model):
    ESTADO_CHOICES = [
        ('publicado', 'Publicado'),
        ('pendiente', 'Pendiente'),
        ('finalizado', 'Finalizado'),
    ]

    titulo = models.CharField(max_length=255)
    archivo_bases = models.FileField(upload_to='oportunidades_trabajo/', blank=True, null=True)
    descripcion = models.TextField()
    activo = models.BooleanField(default=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='publicado')
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

