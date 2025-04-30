from django.urls import path
from .views import servicios_view

urlpatterns = [
     path('', servicios_view, name='servicios'),
]
