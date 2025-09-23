# trabajadores/urls.py

from django.urls import path
from .views import (
    lista_trabajadores,
    buscar_trabajadores_api,
    crear_trabajador,
    editar_trabajador,
    eliminar_trabajador,
)

app_name = 'trabajadores'

urlpatterns = [
    # Vistas de lista y API (mantenerlas)
    path('', lista_trabajadores, name='lista_trabajadores'),
    path('api/buscar/', buscar_trabajadores_api, name='buscar_trabajadores_api'),

    # Nuevas vistas para la gestión
    path('crear/', crear_trabajador, name='crear_trabajador'),
    path('editar/<int:pk>/', editar_trabajador, name='editar_trabajador'),
    path('eliminar/<int:pk>/', eliminar_trabajador, name='eliminar_trabajador'),
]