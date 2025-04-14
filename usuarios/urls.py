from django.urls import path
from . import views

urlpatterns = [
    # Ruta para el registro de un nuevo usuario
    path('registro/', views.registro_usuario, name='registro_usuario'),
    
    # Ruta para mostrar el perfil de usuario
    path('perfil/<int:id>/', views.perfil_usuario, name='perfil_usuario'),
]
