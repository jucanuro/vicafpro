from django.shortcuts import redirect
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib import messages
from django.conf import settings

def contactenos_view(request):
    return render(request, 'contactenos/contactenos.html')

def contacto_view(request):
    if request.method == 'POST':
        name = request.POST['nombre']
        email = request.POST['email']
        subject = request.POST['asunto']
        message = request.POST['mensaje']

        # Renderiza el contenido del correo con tu plantilla HTML
        email_content = render_to_string('contactenos/contacto.html', {
            'name': name,
            'email': email,
            'subject': subject,
            'message': message,
        })

        # Configura y envía el correo
        emailSender = EmailMessage(
            subject,
            email_content,
            settings.EMAIL_HOST_USER,  # Remitente (de tu configuración)
            ['adm.vicaf@gmail.com'],  # Puedes poner múltiples destinatarios aquí
        )
        emailSender.content_subtype = 'html'  # Para que se interprete como HTML
        emailSender.send()

        messages.success(request, "Tu mensaje fue enviado correctamente.")
        return redirect('contactenos')
    
    return redirect('contactenos')


  
def gracias(request):
    return HttpResponse("Gracias por contactarnos. Te responderemos pronto.")
