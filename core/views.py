from django.shortcuts import render
from nosotros.services import obtener_documentos_nosotros
from trabajadores.services import obtener_trabajadores



def index(request):
    context = {}
    context.update(obtener_documentos_nosotros())
    context.update(obtener_trabajadores())

    return render(request, 'index.html', context)