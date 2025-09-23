from django.db import models
from django.utils import timezone
from clientes.models import ClienteProfile
from trabajadores.models import TrabajadorProfile
from servicios.models import Servicio, DetalleServicio, Cotizacion
import os

# ================================================================
#  Funciones de utilidad
# ================================================================
def documento_file_path(instance, filename):
    if instance.proyecto and instance.proyecto.cliente:
        return f'proyectos/documentos/{instance.proyecto.cliente.id}/{instance.proyecto.id}/{filename}'
    return 'proyectos/documentos/default_path/'


# ================================================================
#  Modelos de la aplicación Proyectos
# ================================================================

class Proyecto(models.Model):
    cliente = models.ForeignKey(ClienteProfile, on_delete=models.CASCADE, related_name='proyectos', verbose_name="Cliente")
    cotizacion = models.OneToOneField(Cotizacion, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Cotización Asociada")
    servicios_usados = models.ManyToManyField(Servicio, related_name='proyectos_usados', verbose_name="Servicios Usados")

    nombre_proyecto = models.CharField(max_length=255, verbose_name="Nombre del Proyecto")
    descripcion_proyecto = models.TextField(blank=True, null=True, verbose_name="Descripción del Proyecto")
    
    # CAMPOS CRUCIALES AGREGADOS
    # 'null=True' evita que Django pida un valor por defecto en la consola durante la migración.
    monto_cotizacion = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Monto de la Cotización")
    codigo_voucher = models.CharField(max_length=50, blank=True, null=True, verbose_name="Código del Voucher")
    
    latitud = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True, verbose_name="Latitud")
    longitud = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True, verbose_name="Longitud")
    
    ESTADO_PROYECTO = [
        ('PENDIENTE', 'Pendiente'),
        ('EN_PROGRESO', 'En Progreso'),
        ('FINALIZADO', 'Finalizado'),
        ('CANCELADO', 'Cancelado')
    ]
    estado = models.CharField(max_length=50, choices=ESTADO_PROYECTO, default='PENDIENTE', verbose_name="Estado del Proyecto")
    numero_muestras_total = models.PositiveIntegerField(default=1)
    

    fecha_inicio = models.DateField(default=timezone.now, verbose_name="Fecha de Inicio")
    fecha_fin_estimada = models.DateField(blank=True, null=True, verbose_name="Fecha Fin Estimada")
    fecha_finalizacion_real = models.DateField(blank=True, null=True, verbose_name="Fecha de Finalización Real")

    notificado_cliente = models.BooleanField(default=False, verbose_name="Notificado al Cliente")
    creado_en = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    actualizado_en = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")
    procesado_ia = models.BooleanField(default=False, verbose_name="Procesado por IA")

    def __str__(self):
        return f"{self.nombre_proyecto} ({self.cliente.razon_social})"

    class Meta:
        verbose_name = "Proyecto"
        verbose_name_plural = "Proyectos"
        ordering = ['-creado_en']

class OrdenDeEnsayo(models.Model):
    ESTADOS = [
        ('PENDIENTE', 'Pendiente'),
        ('EN_PROGRESO', 'En Progreso'),
        ('ATRASADO', 'Atrasado'),
        ('FINALIZADO', 'Finalizado'),
        ('RECHAZADO', 'Rechazado'),
    ]

    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='ordenes_de_ensayo', verbose_name="Proyecto")
    codigo_orden = models.CharField(max_length=50, unique=True, verbose_name="Código de la Orden")
    tipo_ensayo = models.CharField(max_length=100, verbose_name="Tipo de Ensayo")
    norma_ensayo = models.CharField(max_length=100, blank=True, null=True, verbose_name="Norma de Ensayo")
    supervisor_asignado = models.ForeignKey(TrabajadorProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='ordenes_supervisadas', verbose_name="Supervisor Asignado")
    fecha_entrega_programada = models.DateField(verbose_name="Fecha de Entrega Programada")
    fecha_entrega_real = models.DateField(blank=True, null=True, verbose_name="Fecha de Entrega Real")
    estado_avance = models.CharField(max_length=20, choices=ESTADOS, default='PENDIENTE', verbose_name="Estado de Avance")

    def __str__(self):
        return f"Orden {self.codigo_orden} para {self.proyecto.nombre_proyecto}"

    class Meta:
        verbose_name = "Orden de Ensayo"
        verbose_name_plural = "Órdenes de Ensayo"
        ordering = ['fecha_entrega_programada']

class Muestra(models.Model):
    # RELACIÓN: Una muestra pertenece a una orden de ensayo. Por lo tanto, un proyecto puede tener muchas muestras a través de la relación OrdenDeEnsayo.
    orden = models.ForeignKey(
        OrdenDeEnsayo,
        on_delete=models.SET_NULL,
        null=True,
        related_name='muestras',
        verbose_name="Orden de Ensayo"
    )
    codigo_muestra = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Código de la Muestra"
    )
    descripcion_muestra = models.TextField(
        verbose_name="Descripción de la Muestra"
    )
    id_lab = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="ID del Laboratorio",
        null=True, blank=True
    )
    tipo_muestra = models.CharField(
        max_length=50,
        verbose_name="Tipo de Muestra (Ej. Concreto, Suelo)",
        default='Sin tipo'
    )
    masa_aprox_kg = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Masa Aproximada (kg)",
        null=True, blank=True
    )
    fecha_recepcion = models.DateField(
        default=timezone.now,
        verbose_name="Fecha de Recepción"
    )
    fecha_fabricacion = models.DateField(
        null=True, blank=True,
        verbose_name="Fecha de Fabricación"
    )
    fecha_ensayo_rotura = models.DateField(
        null=True, blank=True,
        verbose_name="Fecha de Ensayo (solo ensayos de rotura a la compresión)"
    )
    informe = models.CharField(
        max_length=100,
        verbose_name="Código de Informe",
        null=True, blank=True
    )
    fecha_informe = models.DateField(
        null=True, blank=True,
        verbose_name="Fecha de Informe"
    )
    estado = models.CharField(
        max_length=50,
        choices=[('EN CURSO', 'En curso'), ('EN REVISIÓN', 'En revisión'), ('ENVIADO', 'Enviado')],
        verbose_name="Estado de la Muestra",
        default='EN CURSO'
    )
    ensayos_a_realizar = models.TextField(
        verbose_name="Ensayos a realizar",
        null=True, blank=True
    )
    creado_en = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Creación"
    )
    actualizado_en = models.DateTimeField(
        auto_now=True,
        verbose_name="Última Actualización"
    )

    def __str__(self):
        return f"{self.codigo_muestra} - {self.descripcion_muestra}"

    @property
    def cliente(self):
        if self.orden and self.orden.proyecto and self.orden.proyecto.cliente:
            return self.orden.proyecto.cliente
        return None

    class Meta:
        verbose_name = "Muestra"
        verbose_name_plural = "Muestras"
        unique_together = ('orden', 'codigo_muestra')
        ordering = ['-creado_en']
        
class ResultadoEnsayo(models.Model):
    # RELACIÓN: Un resultado de ensayo pertenece a una muestra. Por lo tanto, una muestra puede tener muchos resultados.
    muestra = models.ForeignKey(Muestra, on_delete=models.CASCADE, related_name='resultados', verbose_name="Muestra")
    tecnico_asignado = models.ForeignKey(TrabajadorProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='resultados_realizados', verbose_name="Técnico Asignado")
    resultados_json = models.TextField(blank=True, null=True, verbose_name="Resultados del Ensayo (Descripción)")
    observaciones = models.TextField(blank=True, null=True, verbose_name="Observaciones")
    fecha_realizacion = models.DateField(default=timezone.now, verbose_name="Fecha de Realización")
    
    def __str__(self):
        return f"Resultado de {self.muestra.codigo_muestra}"

    class Meta:
        verbose_name = "Resultado de Ensayo"
        verbose_name_plural = "Resultados de Ensayos"
        ordering = ['-fecha_realizacion']


class DocumentoFinal(models.Model):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='documentos_finales')
    titulo = models.CharField(max_length=255, verbose_name="Título del Documento")
    archivo_original = models.FileField(
        upload_to=documento_file_path,
        blank=True,
        null=True,
        verbose_name="Archivo Escaneado Original (PDF/Imagen)"
    )
    resumen_ejecutivo_ia = models.TextField(blank=True, null=True, verbose_name="Resumen Ejecutivo (IA)")
    analisis_detallado_ia = models.TextField(blank=True, null=True, verbose_name="Análisis Detallado (IA)")
    recomendaciones_ia = models.TextField(blank=True, null=True, verbose_name="Recomendaciones (IA)")
    firma_supervisor = models.ImageField(upload_to='firmas/', blank=True, null=True, verbose_name="Firma del Supervisor")
    firma_cliente = models.ImageField(upload_to='firmas_clientes/', blank=True, null=True, verbose_name="Firma del Cliente")
    fecha_emision = models.DateField(default=timezone.now, verbose_name="Fecha de Emisión")
    
    def __str__(self):
        return f"Documento de {self.proyecto.nombre_proyecto}: {self.titulo}"

    class Meta:
        verbose_name = "Documento Final"
        verbose_name_plural = "Documentos Finales"
        ordering = ['-fecha_emision']

    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='documentos_finales')
    titulo = models.CharField(max_length=255, verbose_name="Título del Documento")
    archivo_original = models.FileField(
        upload_to=documento_file_path,
        blank=True,
        null=True,
        verbose_name="Archivo Escaneado Original (PDF/Imagen)"
    )
    resumen_ejecutivo_ia = models.TextField(blank=True, null=True, verbose_name="Resumen Ejecutivo (IA)")
    analisis_detallado_ia = models.TextField(blank=True, null=True, verbose_name="Análisis Detallado (IA)")
    recomendaciones_ia = models.TextField(blank=True, null=True, verbose_name="Recomendaciones (IA)")
    firma_supervisor = models.ImageField(upload_to='firmas/', blank=True, null=True, verbose_name="Firma del Supervisor")
    firma_cliente = models.ImageField(upload_to='firmas_clientes/', blank=True, null=True, verbose_name="Firma del Cliente")
    fecha_emision = models.DateField(default=timezone.now, verbose_name="Fecha de Emisión")
    
    def __str__(self):
        return f"Documento de {self.proyecto.nombre_proyecto}: {self.titulo}"

    class Meta:
        verbose_name = "Documento Final"
        verbose_name_plural = "Documentos Finales"
        ordering = ['-fecha_emision']