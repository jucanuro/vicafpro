from django.urls import path
from .views import servicios_view, detalleservicios_view

app_name = 'servicios'

urlpatterns = [
     path('', servicios_view, name='servicios'),
     path('detalle/', detalleservicios_view, name='detalle'),
]
