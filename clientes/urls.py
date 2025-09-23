# clientes/urls.py
from django.urls import path
from .views import lista_clientes, crear_editar_cliente, confirmar_eliminar_cliente,  buscar_clientes_api
from .api_views import ClienteProfileListCreateAPIView, ClienteProfileDetailAPIView

app_name = 'clientes'

urlpatterns = [
    # Rutas para el CRUD con HTML
    path('', lista_clientes, name='lista_clientes'),
    path('crear/', crear_editar_cliente, name='crear_cliente'),
    path('editar/<int:pk>/', crear_editar_cliente, name='editar_cliente'),
    path('eliminar/<int:pk>/', confirmar_eliminar_cliente, name='eliminar_cliente'),

    # Rutas para la API REST (manteniendo la separación)
    path('api/clientes/', ClienteProfileListCreateAPIView.as_view(), name='cliente-api-list-create'),
    path('api/clientes/<int:pk>/', ClienteProfileDetailAPIView.as_view(), name='cliente-api-detail'),
    
    path('buscar-api/', buscar_clientes_api, name='buscar_clientes_api'),

]