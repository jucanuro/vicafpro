from django.urls import path
from .views import contactenos_view,contacto_view

urlpatterns = [
    path('', contactenos_view, name='contactenos'),
    path('contactar/', contacto_view, name='contactar'),
]
