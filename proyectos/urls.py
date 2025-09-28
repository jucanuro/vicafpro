from django.urls import path
from . import views

app_name = 'proyectos'

urlpatterns = [
    path('', views.lista_proyectos, name='lista_proyectos'),
    path('crear/', views.crear_proyecto, name='crear_proyecto'),
    path('<int:pk>/editar/', views.editar_proyecto, name='editar_proyecto'),
    path('<int:pk>/eliminar/', views.eliminar_proyecto, name='eliminar_proyecto'),
    path('pendientes/', views.lista_proyectos_pendientes, name='lista_proyectos_pendientes'),
    path('editar/<int:pk>/', views.editar_proyecto_view, name='editar_proyecto_api'),
    
    path('crear-muestra/', views.create_and_edit_muestra, name='crear_muestra'),
    path('muestras/<int:proyecto_id>/', views.muestras_del_proyecto, name='muestras_del_proyecto'),
    
    
    path('ordenes/registrar/<int:orden_id>/', views.orden_de_ensayo_form, name='orden_ensayo_form'), 

    path('documento/<int:pk>/', views.orden_de_ensayo_documento, name='orden_ensayo_documento'),
    path('resultados/registrar/<int:muestra_pk>/', views.registro_resultado_form, name='registro_resultado_form'),
 
]
