# servicios/admin.py
from django.contrib import admin
from .models import (
    Servicio,
    DetalleServicio,
    Cotizacion,
    CotizacionDetalle,
    Voucher,
    Norma,
    Metodo
)

# Registramos los modelos simples
admin.site.register(Norma)
admin.site.register(Metodo)
admin.site.register(Voucher)
admin.site.register(DetalleServicio)


class CotizacionDetalleInline(admin.TabularInline):
    model = CotizacionDetalle
    extra = 1

@admin.register(Cotizacion)
class CotizacionAdmin(admin.ModelAdmin):
    inlines = [CotizacionDetalleInline]
    # Corregido: list_display ahora usa un método para acceder a la razón social del cliente
    list_display = (
        'numero_oferta',
        'get_cliente_razon_social', # Método corregido
        'fecha_creacion',
        'estado',
        'monto_total'
    )
    list_filter = ('estado', 'fecha_creacion')
    search_fields = ('numero_oferta', 'cliente__razon_social', 'cliente__ruc')
    readonly_fields = ('fecha_creacion',)

    # Método para obtener la razón social del cliente
    def get_cliente_razon_social(self, obj):
        return obj.cliente.razon_social
    
    # Configuramos el nombre de la columna en el Admin
    get_cliente_razon_social.short_description = 'Razón Social'


@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'orden', 'get_normas', 'get_metodos')
    list_filter = ('normas', 'metodos')
    search_fields = ('nombre', 'descripcion')
    list_editable = ('orden',)

    def get_normas(self, obj):
        return ", ".join([norma.nombre for norma in obj.normas.all()])
    
    get_normas.short_description = "Normas"

    def get_metodos(self, obj):
        return ", ".join([metodo.nombre for metodo in obj.metodos.all()])

    get_metodos.short_description = "Métodos"