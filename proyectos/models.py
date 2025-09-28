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


class Proyecto(models.Model):
    # Relación con Cotizacion
    cotizacion = models.ForeignKey(Cotizacion, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Cotización")
    
    ESTADOS_PROYECTO = [
        ('PENDIENTE', 'Pendiente'),
        ('EN_CURSO', 'En Curso'),
        ('FINALIZADO', 'Finalizado'),
        ('CANCELADO', 'Cancelado'),
    ]

    nombre_proyecto = models.CharField(max_length=255, verbose_name="Nombre del Proyecto")
    codigo_proyecto = models.CharField(max_length=50, unique=True, verbose_name="Código del Proyecto")
    cliente = models.ForeignKey(ClienteProfile, on_delete=models.CASCADE, verbose_name="Cliente", related_name='proyectos')
    
    # -----------------------------------------------------------
    # 🆕 CAMPOS AGREGADOS (Solución al TypeError)
    # -----------------------------------------------------------
    descripcion_proyecto = models.TextField(verbose_name="Descripción", blank=True, null=True)
    monto_cotizacion = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Monto de la Cotización")
    codigo_voucher = models.CharField(max_length=100, verbose_name="Código de Voucher/Operación", blank=True, null=True)
    # -----------------------------------------------------------

    fecha_inicio = models.DateField(default=timezone.now, verbose_name="Fecha de Inicio")
    fecha_entrega_estimada = models.DateField(blank=True, null=True, verbose_name="Fecha de Entrega Estimada")
    estado = models.CharField(max_length=20, choices=ESTADOS_PROYECTO, default='PENDIENTE', verbose_name="Estado")
    
    # Campo para el número total de muestras del proyecto (ya existía)
    numero_muestras = models.PositiveIntegerField(default=0, verbose_name="Número de Muestras")
    # Campo para el número de muestras registradas (ya existía)
    numero_muestras_registradas = models.PositiveIntegerField(default=0, verbose_name="Número de Muestras Registradas")

    creado_en = models.DateTimeField(auto_now_add=True)
    modificado_en = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre_proyecto} ({self.codigo_proyecto})"

    class Meta:
        verbose_name = "Proyecto"
        verbose_name_plural = "Proyectos"
        ordering = ['-creado_en']


class Muestra(models.Model):
    ESTADOS_MUESTRA = [
        ('RECIBIDA', 'Recibida'),
        ('EN_ANALISIS', 'En Análisis'),
        ('INFORME_FINAL', 'Informe Final'),
        ('VALIDADO', 'Validado'),
    ]

    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='muestras', verbose_name="Proyecto")
    codigo_muestra = models.CharField(max_length=100, verbose_name="Código de Muestra")
    descripcion_muestra = models.TextField(blank=True, null=True, verbose_name="Descripción de la Muestra")
    id_lab = models.CharField(max_length=50, blank=True, null=True, verbose_name="ID de Laboratorio")
    tipo_muestra = models.CharField(max_length=100, blank=True, null=True, verbose_name="Tipo de Muestra")
    masa_aprox_kg = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Masa Aprox. (kg)")
    fecha_recepcion = models.DateField(default=timezone.now, verbose_name="Fecha de Recepción")
    fecha_fabricacion = models.DateField(blank=True, null=True, verbose_name="Fecha de Fabricación")
    fecha_ensayo_rotura = models.DateField(blank=True, null=True, verbose_name="Fecha de Ensayo de Rotura")
    informe = models.TextField(blank=True, null=True, verbose_name="Informe")
    fecha_informe = models.DateField(blank=True, null=True, verbose_name="Fecha de Informe")
    estado = models.CharField(max_length=20, choices=ESTADOS_MUESTRA, default='RECIBIDA', verbose_name="Estado")
    
    # Campo para los ensayos a realizar, si es necesario
    ensayos_a_realizar = models.TextField(blank=True, null=True, verbose_name="Ensayos a Realizar")

    creado_en = models.DateTimeField(auto_now_add=True)
    modificado_en = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.codigo_muestra} - {self.proyecto.nombre_proyecto}"

    class Meta:
        verbose_name = "Muestra"
        verbose_name_plural = "Muestras"
        unique_together = ('proyecto', 'codigo_muestra')

class OrdenDeEnsayo(models.Model):
    # La Orden de Ensayo debe estar vinculada a una Muestra y a un Proyecto
    muestra = models.ForeignKey(Muestra, on_delete=models.CASCADE, related_name='ordenes', verbose_name="Muestra")
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='ordenes', verbose_name="Proyecto")

    # --- Campos para el Documento de Trabajo ---
    tipo_ensayo = models.CharField(max_length=100, verbose_name="Tipo de Ensayo")
    fecha_entrega_programada = models.DateField(verbose_name="Fecha de Entrega Programada")
    
    # Campo para asignar el técnico responsable de esta orden
    tecnico_asignado = models.ForeignKey(
        TrabajadorProfile, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='ordenes_asignadas', 
        verbose_name="Técnico Asignado"
    )
    
    # Estado de la Orden de Ensayo (para saber si ya se registraron los resultados)
    ESTADOS = (
        ('PENDIENTE', 'Pendiente de Inicio'),
        ('EN_PROCESO', 'En Proceso de Ensayo'),
        ('RESULTADOS_REGISTRADOS', 'Resultados Registrados'),
        ('REVISADA', 'Revisada/Cerrada')
    )
    estado_orden = models.CharField(max_length=50, choices=ESTADOS, default='PENDIENTE', verbose_name="Estado de la Orden")
    
    # Información de auditoría
    creado_en = models.DateTimeField(auto_now_add=True)
    modificado_en = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Orden de Ensayo para {self.muestra.codigo_muestra}"

    class Meta:
        verbose_name = "Orden de Ensayo"
        verbose_name_plural = "Órdenes de Ensayo"
        
        
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