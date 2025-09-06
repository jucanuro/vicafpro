# proyectos/urls.py
# Este archivo es crucial para definir las rutas (endpoints) de la API REST.

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .api_views import (
    ProyectoViewSet, 
    OrdenDeEnsayoViewSet, 
    MuestraViewSet, 
    ResultadoEnsayoViewSet, 
    DocumentoFinalViewSet, 
    ServicioViewSet
)

from .views import proyectos_view, home_view, crear_proyecto_view

app_name = 'proyectos'

router = DefaultRouter()
router.register(r'proyectos', ProyectoViewSet, basename='proyecto')
router.register(r'ordenes-de-ensayo', OrdenDeEnsayoViewSet, basename='orden-de-ensayo')
router.register(r'muestras', MuestraViewSet, basename='muestra')
router.register(r'resultados-ensayo', ResultadoEnsayoViewSet, basename='resultado-ensayo')
router.register(r'documentos-finales', DocumentoFinalViewSet, basename='documento-final')
router.register(r'servicios', ServicioViewSet, basename='servicio')


urlpatterns = [
    # Incluimos todas las URLs generadas por el router.
    path('', home_view, name='proyectos_principal'),
    path('lista/', proyectos_view, name='lista_proyectos'),
    path('crear/', crear_proyecto_view, name='crear_proyecto'),
    
    path('ordenes/', views.orden_de_ensayo_list, name='orden_de_ensayo_list'),
    path('ordenes/crear/', views.orden_de_ensayo_create, name='orden_de_ensayo_create'),
    path('ordenes/<int:pk>/editar/', views.orden_de_ensayo_update, name='orden_de_ensayo_update'),
    path('ordenes/<int:pk>/eliminar/', views.orden_de_ensayo_delete, name='orden_de_ensayo_delete'),

    # URLs para Muestra
    path('muestras/', views.muestra_list, name='muestra_list'),
    path('muestras/crear/', views.muestra_create, name='muestra_create'),
    path('muestras/<int:pk>/editar/', views.muestra_update, name='muestra_update'),
    path('muestras/<int:pk>/eliminar/', views.muestra_delete, name='muestra_delete'),
    
    # URLs para Resultado de Ensayo
    path('resultados/', views.resultado_ensayo_list, name='resultado_ensayo_list'),
    path('resultados/crear/', views.resultado_ensayo_create, name='resultado_ensayo_create'),
    path('resultados/<int:pk>/editar/', views.resultado_ensayo_update, name='resultado_ensayo_update'),
    path('resultados/<int:pk>/eliminar/', views.resultado_ensayo_delete, name='resultado_ensayo_delete'),
    
    # URLs para Documento Final
    path('documentos/', views.documento_final_list, name='documento_final_list'),
    path('documentos/crear/', views.documento_final_create, name='documento_final_create'),
    path('documentos/<int:pk>/editar/', views.documento_final_update, name='documento_final_update'),
    path('documentos/<int:pk>/eliminar/', views.documento_final_delete, name='documento_final_delete'),

    path('documentos/<int:pk>/pdf/', views.documento_final_pdf, name='documento_final_pdf'),

    
    path('api/', include(router.urls)),
]

