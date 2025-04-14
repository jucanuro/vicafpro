from django.shortcuts import render
from django.views.generic import ListView
from .models import Cliente

class ClienteListView(ListView):
    model = Cliente
    template_name = 'clientes/clientes.html'  # Plantilla para mostrar los clientes
    context_object_name = 'clientes'  # Nombre que usaremos para acceder a los objetos en la plantilla
    paginate_by = 10  # Número de clientes por página
