# trabajadores/urls.py
from django.urls import path
from .views import (
    trabajadores_view,
    TrabajadorListView,
    TrabajadorDetailView,
    TrabajadorCreateView,
    TrabajadorUpdateView,
    TrabajadorDeleteView
)

urlpatterns = [
    # Vista principal del módulo
    path('', trabajadores_view, name='trabajadores'),

    # Rutas para el CRUD de Trabajadores
    path('lista/', TrabajadorListView.as_view(), name='trabajador_list'),
    path('crear/', TrabajadorCreateView.as_view(), name='trabajador_create'),
    path('<int:pk>/', TrabajadorDetailView.as_view(), name='trabajador_detail'),
    path('<int:pk>/editar/', TrabajadorUpdateView.as_view(), name='trabajador_update'),
    path('<int:pk>/eliminar/', TrabajadorDeleteView.as_view(), name='trabajador_delete'),
]