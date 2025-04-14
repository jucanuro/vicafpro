from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import MensajeContacto
from django.core.mail import send_mail
from django.conf import settings

def contacto(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        correo = request.POST.get('correo')
        asunto = request.POST.get('asunto')
        mensaje = request.POST.get('mensaje')

        # Crear el mensaje de contacto
        nuevo_mensaje = MensajeContacto(
            nombre=nombre,
            correo=correo,
            asunto=asunto,
            mensaje=mensaje
        )
        nuevo_mensaje.save()

        # Enviar el correo al administrador
        nuevo_mensaje.enviar_correo()

        # Redirigir a una página de agradecimiento
        return redirect('gracias')

    return render(request, 'contactenos/contacto.html')


def gracias(request):
    return HttpResponse("Gracias por contactarnos. Te responderemos pronto.")
