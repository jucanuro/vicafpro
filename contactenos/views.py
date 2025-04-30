from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import MensajeContacto
from django.core.mail import send_mail
from django.conf import settings

def contactenos_view(request):
    return render(request, 'contactenos/contactenos.html')

def contacto_view(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        correo = request.POST['correo']
        asunto = request.POST['asunto']
        mensaje = request.POST['mensaje']

        mensaje_obj = MensajeContacto.objects.create(
            nombre=nombre,
            correo=correo,
            asunto=asunto,
            mensaje=mensaje
        )

        mensaje_obj.enviar_correo()

        return redirect('gracias')  # redirige a una página de agradecimiento

    return render(request, 'contacto.html')


def gracias(request):
    return HttpResponse("Gracias por contactarnos. Te responderemos pronto.")
