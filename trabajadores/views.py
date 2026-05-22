from django.shortcuts import render
from .models import Trabajador


def trabajadores_view(request):
    trabajadores = Trabajador.objects.all()
    return render(request, 'trabajadores/trabajadores.html',{
        'trabajadores',trabajadores
    })
