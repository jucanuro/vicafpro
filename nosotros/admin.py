from django.contrib import admin
from .models import Nosotros, TipoDocumentoNosotros, DocumentoNosotros


@admin.register(Nosotros)
class NosotrosAdmin(admin.ModelAdmin):
    list_display = ('titulo',)
    search_fields = ('titulo', 'contenido')


@admin.register(TipoDocumentoNosotros)
class TipoDocumentoNosotrosAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        'slug',
        'activo',
        'orden',
        'actualizado',
    )

    list_editable = (
        'activo',
        'orden',
    )

    search_fields = (
        'nombre',
        'slug',
        'descripcion',
    )

    list_filter = (
        'activo',
    )

    prepopulated_fields = {
        'slug': ('nombre',),
    }

    ordering = (
        'orden',
        'nombre',
    )

    readonly_fields = (
        'creado',
        'actualizado',
    )

    fieldsets = (
        ('Información del tipo', {
            'fields': (
                'nombre',
                'slug',
                'descripcion',
            )
        }),
        ('Configuración', {
            'fields': (
                'activo',
                'orden',
            )
        }),
        ('Auditoría', {
            'fields': (
                'creado',
                'actualizado',
            ),
            'classes': ('collapse',),
        }),
    )


@admin.register(DocumentoNosotros)
class DocumentoNosotrosAdmin(admin.ModelAdmin):
    list_display = (
        'titulo',
        'tipo',
        'activo',
        'destacado',
        'orden',
        'fecha_publicacion',
        'actualizado',
    )

    list_filter = (
        'tipo',
        'activo',
        'destacado',
        'fecha_publicacion',
    )

    search_fields = (
        'titulo',
        'descripcion',
        'tipo__nombre',
    )

    list_editable = (
        'activo',
        'destacado',
        'orden',
    )

    list_select_related = (
        'tipo',
    )

    ordering = (
        'orden',
        '-destacado',
        '-creado',
    )

    readonly_fields = (
        'creado',
        'actualizado',
    )

    autocomplete_fields = (
        'tipo',
    )

    date_hierarchy = 'fecha_publicacion'

    fieldsets = (
        ('Información principal', {
            'fields': (
                'tipo',
                'titulo',
                'descripcion',
            )
        }),
        ('Archivos del documento', {
            'fields': (
                'imagen',
                'archivo',
            )
        }),
        ('Configuración de visualización', {
            'fields': (
                'activo',
                'destacado',
                'orden',
                'fecha_publicacion',
            )
        }),
        ('Auditoría', {
            'fields': (
                'creado',
                'actualizado',
            ),
            'classes': ('collapse',),
        }),
    )