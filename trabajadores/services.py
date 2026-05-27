from django.db.models import Prefetch

from .models import (
    AreaOrganizacional,
    Cargo,
    Trabajador
)


def obtener_trabajadores():

    trabajadores_queryset = Trabajador.objects.filter(
        activo=True
    ).select_related(
        'cargo',
        'cargo__area'
    ).order_by(
        'orden',
        'nombre'
    )

    cargos_queryset = Cargo.objects.filter(
        activo=True
    ).select_related(
        'area'
    ).prefetch_related(
        Prefetch(
            'trabajadores',
            queryset=trabajadores_queryset
        )
    ).order_by(
        'orden',
        'nombre'
    )

    areas = AreaOrganizacional.objects.filter(
        activo=True
    ).prefetch_related(
        Prefetch(
            'cargos',
            queryset=cargos_queryset
        )
    ).order_by(
        'orden',
        'nombre'
    )

    return {
        'areas': areas
    }