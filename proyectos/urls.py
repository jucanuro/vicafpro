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
]
