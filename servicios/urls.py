# servicios/urls.py
from django.urls import path
from . import views

app_name = 'servicios'

urlpatterns = [
    # URLs para las vistas del sitio web
    path('web/servicios/', views.servicios_view, name='servicios_view'),
    path('web/detalles/', views.detalle_servicios_view, name='detalle_servicios_view'),
    
    # URLs Servicios
    path('', views.lista_servicios, name='lista_servicios'),
    path('crear/', views.crear_servicio, name='crear_servicio'),
    path('editar/<int:pk>/', views.editar_servicio, name='editar_servicio'),
    path('eliminar/<int:pk>/', views.eliminar_servicio, name='eliminar_servicio'),
    
    # URLs Cotizaciones
    
    path('cotizaciones/', views.lista_cotizaciones, name='lista_cotizaciones'),
    path('cotizaciones/crear/', views.crear_cotizacion, name='crear_cotizacion'),
    path('cotizaciones/editar/<int:pk>/', views.editar_cotizacion, name='editar_cotizacion'),
    path('cotizaciones/eliminar/<int:pk>/', views.eliminar_cotizacion, name='eliminar_cotizacion'),
    path('cotizaciones/api/buscar/', views.buscar_cotizaciones_api, name='buscar_cotizaciones_api'),
    
    path('cotizaciones/<int:pk>/pdf/', views.generar_pdf_cotizacion, name='ver_pdf_cotizacion'),
    path('cotizaciones/<int:pk>/aprobar/', views.aprobar_cotizacion, name='aprobar_cotizacion'),


    
    path('cotizaciones/api/servicios/<int:pk>/', views.obtener_detalle_servicio_para_cotizacion_api, name='obtener_detalle_servicio_para_cotizacion_api'),

    path('api/ver/<int:pk>/', views.obtener_detalle_servicio_api, name='obtener_detalle_servicio_api'),
    path('api/buscar/', views.buscar_servicios_api, name='buscar_servicios_api'),
]