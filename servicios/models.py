# servicios/models.py
from django.db import models
from django.utils import timezone
from clientes.models import ClienteProfile
from trabajadores.models import TrabajadorProfile
from decimal import Decimal
from django.core.validators import FileExtensionValidator

# ================================================================
#   Modelos para la gestión de servicios web (no modificados)
# ================================================================
class Norma(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class Metodo(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class Servicio(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre del Servicio")
    descripcion = models.TextField(verbose_name="Descripción del Servicio")
    normas = models.ManyToManyField(Norma, related_name='servicios', blank=True)
    metodos = models.ManyToManyField(Metodo, related_name='servicios', blank=True)
    imagen = models.ImageField(upload_to='servicios/', verbose_name="Imagen")
    orden = models.PositiveIntegerField(default=0, verbose_name="Orden")

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Servicio Web"
        verbose_name_plural = "Servicios Web"
        ordering = ['orden']


class DetalleServicio(models.Model):
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, related_name='detalles', verbose_name="Servicio")
    titulo = models.CharField(max_length=100, verbose_name="Título del Detalle")
    descripcion = models.TextField(verbose_name="Descripción del Detalle")
    imagen = models.ImageField(upload_to='servicios/detalles/', blank=True, null=True, verbose_name="Imagen")

    def __str__(self):
        return f"{self.servicio.nombre} - {self.titulo}"

    class Meta:
        verbose_name = "Detalle de Servicio"
        verbose_name_plural = "Detalles de Servicios"


# ================================================================
#   Nuevo modelo de Cotización, optimizado para la lógica de negocio
# ================================================================
class Cotizacion(models.Model):
    cliente = models.ForeignKey(ClienteProfile, on_delete=models.CASCADE, related_name='cotizaciones', default=1)
    numero_oferta = models.CharField(max_length=50, unique=True)
    persona_contacto = models.CharField(max_length=200)
    correo_contacto = models.EmailField()
    telefono_contacto = models.CharField(max_length=20)
    
    ESTADO_CHOICES = [
        ('Pendiente', 'Pendiente de Aprobación'),
        ('Aceptada', 'Aceptada'),
        ('Rechazada', 'Rechazada'),
    ]
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Pendiente')
    
    plazo_entrega_dias = models.IntegerField(default=0)
    FORMA_PAGO_CHOICES = [
        ('Contado', 'Al Contado'),
        ('15_dias', 'A 15 días'),
        ('30_dias', 'A 30 días'),
        ('3_meses', 'A 3 meses'),
    ]
    forma_pago = models.CharField(max_length=20, choices=FORMA_PAGO_CHOICES, default='Contado')
    validez_oferta_dias = models.IntegerField(default=30)
    
    monto_total = models.DecimalField(max_digits=10, decimal_places=2,  default=Decimal('0.00'))
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return self.numero_oferta
# ================================================================
#   Nuevo modelo para el detalle de la cotización
# ================================================================
class CotizacionDetalle(models.Model):
    cotizacion = models.ForeignKey(Cotizacion, on_delete=models.CASCADE, related_name='detalles_cotizacion', verbose_name="Cotización")
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, verbose_name="Servicio")
    
    # -----------------------------------------------------------
    # CORRECCIÓN: Agregar campos para Norma y Metodo
    # -----------------------------------------------------------
    norma = models.ForeignKey('Norma', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Norma de Ensayo")
    metodo = models.ForeignKey('Metodo', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Método")
    und = models.CharField(max_length=50, default='und')
    cantidad = models.PositiveIntegerField(default=1, verbose_name="Cantidad")
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio Unitario")
    
    @property
    def subtotal(self):
        return self.cantidad * self.precio_unitario

    def __str__(self):
        return f"Detalle de Cotización para {self.cotizacion.numero_oferta}"

    class Meta:
        verbose_name = "Detalle de Cotización"
        verbose_name_plural = "Detalles de Cotización"
        

class Voucher(models.Model):
    cotizacion = models.OneToOneField(Cotizacion, on_delete=models.CASCADE, related_name='voucher')
    codigo = models.CharField(max_length=100)
    imagen = models.ImageField(
        upload_to='vouchers/',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'pdf'])]
    )
    fecha_subida = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Voucher para Cotización {self.cotizacion.numero_oferta}'
        
    
