from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario

# Vista para el registro de usuario
def registro_usuario(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)  # Iniciar sesión al registrarse
            return redirect('perfil_usuario', id=usuario.id)
    else:
        form = UserCreationForm()
    return render(request, 'usuarios/registro.html', {'form': form})

# Vista para mostrar el perfil de usuario
def perfil_usuario(request, id):
    try:
        usuario = Usuario.objects.get(id=id)
    except Usuario.DoesNotExist:
        return redirect('home')  # Si no existe, redirigir al inicio

    return render(request, 'usuarios/perfil.html', {'usuario': usuario})
