from django.shortcuts import render
from nosotros.services import obtener_documentos_nosotros


def index(request):
    context = {}
    context.update(obtener_documentos_nosotros())

    return render(request, 'index.html', context)