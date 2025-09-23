# trabajadores/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import TrabajadorProfile

User = get_user_model()

def is_admin(user):
    try:
        return user.is_authenticated and user.trabajadorprofile.role == 'ADMINISTRADOR'
    except TrabajadorProfile.DoesNotExist:
        return False

@login_required
@user_passes_test(is_admin)
def crear_trabajador(request):
    if request.method == 'POST':
        # Obtener los datos del formulario directamente del POST
        nombre_completo = request.POST.get('nombre_completo')
        email = request.POST.get('email')
        role = request.POST.get('role')
        
        # Validación básica del lado del servidor
        if not nombre_completo or not email or not role:
            return render(request, 'trabajadores/trabajadores_form.html', {
                'error': 'Todos los campos son obligatorios.'
            })
        
        # Crear un usuario de Django y el perfil de trabajador
        try:
            user = User.objects.create_user(username=email, email=email)
            TrabajadorProfile.objects.create(
                user=user,
                nombre_completo=nombre_completo,
                role=role
            )
            return redirect('trabajadores:lista_trabajadores')
        except Exception as e:
            return render(request, 'trabajadores/trabajadores_form.html', {
                'error': f'Ocurrió un error al crear el trabajador: {e}'
            })

    return render(request, 'trabajadores/trabajadores_form.html')

@login_required
@user_passes_test(is_admin)
def editar_trabajador(request, pk):
    trabajador = get_object_or_404(TrabajadorProfile, pk=pk)
    if request.method == 'POST':
        # Obtener datos del formulario
        nombre_completo = request.POST.get('nombre_completo')
        email = request.POST.get('email')
        role = request.POST.get('role')

        if not nombre_completo or not email or not role:
            return render(request, 'trabajadores/trabajadores_form.html', {
                'trabajador': trabajador,
                'error': 'Todos los campos son obligatorios.'
            })

        trabajador.nombre_completo = nombre_completo
        trabajador.role = role
        trabajador.user.email = email
        trabajador.user.username = email
        
        trabajador.save()
        trabajador.user.save()

        return redirect('trabajadores:lista_trabajadores')

    return render(request, 'trabajadores/trabajadores_form.html', {'trabajador': trabajador})

@login_required
@user_passes_test(is_admin)
def eliminar_trabajador(request, pk):
    trabajador = get_object_or_404(TrabajadorProfile, pk=pk)
    if request.method == 'POST':
        # Se elimina el objeto user, lo que activará la eliminación en cascada del TrabajadorProfile
        trabajador.user.delete()
        return redirect('trabajadores:lista_trabajadores')
    
    return render(request, 'trabajadores/confirmar_eliminar_trabajador.html', {'trabajador': trabajador})

# --- Mantener las vistas de lista y API que ya tenías ---
def lista_trabajadores(request):
    query = request.GET.get('q')
    trabajadores = TrabajadorProfile.objects.all()

    if query:
        trabajadores = trabajadores.filter(
            Q(nombre_completo__icontains=query) |
            Q(role__icontains=query) |
            Q(user__email__icontains=query)
        ).distinct()

    paginator = Paginator(trabajadores, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'trabajadores': page_obj,
        'query': query,
    }
    return render(request, 'trabajadores/trabajadores_list.html', context)


def buscar_trabajadores_api(request):
    query = request.GET.get('q', '')
    trabajadores = TrabajadorProfile.objects.filter(
        Q(nombre_completo__icontains=query) |
        Q(role__icontains=query) |
        Q(user__email__icontains=query)
    ).select_related('user').values(
        'pk', 
        'nombre_completo', 
        'role',
        'creado_en',
        'user__email'
    )[:10]

    for trabajador in trabajadores:
        trabajador['creado_en'] = trabajador['creado_en'].strftime("%d %b %Y")
        trabajador['email'] = trabajador.pop('user__email')

    return JsonResponse(list(trabajadores), safe=False)