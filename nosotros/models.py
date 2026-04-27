import os
from django.db import models


class Nosotros(models.Model):
    titulo = models.CharField(max_length=100)
    contenido = models.TextField()
    imagen = models.ImageField(upload_to='nosotros/', blank=True, null=True)

    class Meta:
        verbose_name = 'Nosotros'
        verbose_name_plural = 'Nosotros'

    def __str__(self):
        return self.titulo


class TipoDocumentoNosotros(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    orden = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)

    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Tipo de Documento'
        verbose_name_plural = 'Tipos de Documentos'
        ordering = ['orden', 'nombre']

    def __str__(self):
        return self.nombre


class DocumentoNosotros(models.Model):
    tipo = models.ForeignKey(
        TipoDocumentoNosotros,
        on_delete=models.PROTECT,
        related_name='documentos'
    )

    titulo = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True, null=True)

    imagen = models.ImageField(
        upload_to='nosotros/documentos/imagenes/',
        blank=True,
        null=True,
        help_text='Imagen de portada o miniatura del documento.'
    )

    archivo = models.FileField(
        upload_to='nosotros/documentos/archivos/',
        help_text='Subir PDF, imagen, Word, Excel o PowerPoint.'
    )

    orden = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)
    destacado = models.BooleanField(
        default=False,
        help_text='Marcar si deseas priorizar este documento entre los primeros visibles.'
    )

    fecha_publicacion = models.DateField(blank=True, null=True)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Documento de Nosotros'
        verbose_name_plural = 'Documentos de Nosotros'
        ordering = ['orden', '-destacado', '-creado']

    def __str__(self):
        return f'{self.tipo.nombre} - {self.titulo}'

    @property
    def extension_archivo(self):
        if not self.archivo:
            return ''
        return os.path.splitext(self.archivo.name)[1].lower()

    @property
    def es_imagen(self):
        return self.extension_archivo in ['.jpg', '.jpeg', '.png', '.webp', '.gif']

    @property
    def es_pdf(self):
        return self.extension_archivo == '.pdf'

    @property
    def es_office(self):
        return self.extension_archivo in [
            '.doc',
            '.docx',
            '.xls',
            '.xlsx',
            '.ppt',
            '.pptx',
        ]
        
    @property
    def es_certificado(self):
        nombre_tipo = self.tipo.nombre.lower() if self.tipo else ''
        return 'certificado' in nombre_tipo