# servicios/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .api_views import CotizacionViewSet

# Importamos solo las vistas que vamos a usar
from .views import (
    servicios_view,
    detalle_servicios_view,
    ServicioListView,
    ServicioDetailView,
    ServicioDeleteView,
    servicio_create_or_update, # Vista unificada
)

app_name = 'servicios'

# Creamos el router para la API de Cotizaciones (si aún la usas)
router = DefaultRouter()
router.register(r'cotizaciones', CotizacionViewSet)

urlpatterns = [
    # URLs de tus vistas web principales
    path('', servicios_view, name='servicios'),
    path('detalle/', detalle_servicios_view, name='servicios-detalle'),

    # URLs para la gestión de Servicios (CRUD)
    path('lista/', ServicioListView.as_view(), name='servicio_list'),
    path('crear/', servicio_create_or_update, name='servicio_create'),
    path('<int:pk>/', ServicioDetailView.as_view(), name='servicio_detail'),
    path('editar/<int:pk>/', servicio_create_or_update, name='servicio_update'),
    path('eliminar/<int:pk>/', ServicioDeleteView.as_view(), name='servicio_delete'),

    # URLs para la gestión de Cotizaciones (panel de administración)
    # Ya no se necesita CotizacionListView
    
    # URLs de la API para la cotización
    path('api/cotizaciones/crear/', views.crear_cotizacion, name='crear_cotizacion'),
    path('api/buscar-cliente/', views.buscar_cliente, name='buscar_cliente'),
    path('api/buscar-servicio/', views.buscar_servicio, name='buscar_servicio'),
    path('api/servicio/<int:servicio_id>/detalles/', views.obtener_detalles_servicio, name='obtener_detalles_servicio'),

    # URLs para el flujo del cliente
    path('cotizacion/<str:numero_oferta>/', views.ver_cotizacion, name='ver_cotizacion'),
    path('cotizacion/<int:cotizacion_id>/aceptar/', views.aceptar_cotizacion, name='aceptar_cotizacion'),
    path('cotizacion/<int:cotizacion_id>/rechazar/', views.rechazar_cotizacion, name='rechazar_cotizacion'),
    path('cotizacion/<int:cotizacion_id>/subir-voucher/', views.subir_voucher, name='subir_voucher'),
    
        path('cotizaciones/', views.CotizacionListView.as_view(), name='cotizacion_list'),


    # Incluye las URLs del router de DRF
    path('api/', include(router.urls)),
]