from django.contrib import admin
from django.utils.html import format_html

from .models import (
    AreaOrganizacional,
    Cargo,
    Trabajador
)



@admin.register(AreaOrganizacional)
class AreaOrganizacionalAdmin(admin.ModelAdmin):

    list_display = (
        'orden',
        'nombre',
        'total_cargos',
        'activo',
    )

    list_display_links = (
        'nombre',
    )

    list_editable = (
        'orden',
        'activo',
    )

    search_fields = (
        'nombre',
    )

    list_filter = (
        'activo',
    )

    ordering = (
        'orden',
        'nombre',
    )

    fieldsets = (
        (
            'Información del Área',
            {
                'fields': (
                    'nombre',
                    'orden',
                    'activo',
                )
            }
        ),
    )

    def total_cargos(self, obj):
        return obj.cargos.count()

    total_cargos.short_description = 'Cargos'




@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):

    list_display = (
        'orden',
        'nombre',
        'area',
        'total_trabajadores',
        'activo',
    )

    list_display_links = (
        'nombre',
    )

    list_editable = (
        'orden',
        'activo',
    )

    search_fields = (
        'nombre',
        'area__nombre',
    )

    list_filter = (
        'area',
        'activo',
    )

    ordering = (
        'area__orden',
        'orden',
        'nombre',
    )

    autocomplete_fields = (
        'area',
    )

    fieldsets = (
        (
            'Información del Cargo',
            {
                'fields': (
                    'area',
                    'nombre',
                    'orden',
                    'activo',
                )
            }
        ),
    )

    def total_trabajadores(self, obj):
        return obj.trabajadores.count()

    total_trabajadores.short_description = 'Trabajadores'




@admin.register(Trabajador)
class TrabajadorAdmin(admin.ModelAdmin):

    list_display = (
        'preview_foto',
        'nombre',
        'area_organizacional',
        'cargo',
        'orden',
        'email',
        'activo',
    )

    list_display_links = (
        'preview_foto',
        'nombre',
    )

    list_editable = (
        'cargo',
        'orden',
        'activo',
    )

    search_fields = (
        'nombre',
        'email',
        'cargo__nombre',
        'cargo__area__nombre',
    )

    list_filter = (
        'cargo__area',
        'cargo',
        'activo',
    )

    ordering = (
        'cargo__area__orden',
        'cargo__orden',
        'orden',
        'nombre',
    )

    autocomplete_fields = (
        'cargo',
    )

    fieldsets = (

        (
            'Información Organizacional',
            {
                'fields': (
                    'cargo',
                    'orden',
                    'activo',
                )
            }
        ),

        (
            'Información Personal',
            {
                'fields': (
                    'nombre',
                    'foto',
                )
            }
        ),

        (
            'Información de Contacto',
            {
                'fields': (
                    'email',
                    'linkedin',
                )
            }
        ),

    )


    def preview_foto(self, obj):

        if obj.foto:
            return format_html(
                '''
                <img 
                    src="{}"
                    style="
                        width:52px;
                        height:52px;
                        border-radius:50%;
                        object-fit:cover;
                        border:2px solid #e2e8f0;
                        box-shadow:0 4px 10px rgba(0,0,0,.08);
                    "
                />
                ''',
                obj.foto.url
            )

        return "—"

    preview_foto.short_description = 'Foto'


    def area_organizacional(self, obj):

        if obj.cargo and obj.cargo.area:
            return obj.cargo.area.nombre

        return "—"

    area_organizacional.short_description = 'Área'