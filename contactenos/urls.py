from django.urls import path
from . import views

urlpatterns = [
    path('', views.contacto, name='contacto'),
    path('gracias/', views.gracias, name='gracias'),  # Redirigir después de enviar el mensaje
]
