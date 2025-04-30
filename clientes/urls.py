from django.urls import path
from .views import clientes_view

urlpatterns = [
    path('', clientes_view, name='clientes'),
]