# clientes/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator
from .models import ClienteProfile


def lista_clientes(request):
    query = request.GET.get('q')
    clientes = ClienteProfile.objects.all()

    if query:
        clientes = clientes.filter(
            Q(razon_social__icontains=query) |
            Q(ruc__icontains=query) |
            Q(persona_contacto__icontains=query) |
            Q(correo_contacto__icontains=query)
        ).distinct()

    paginator = Paginator(clientes, 10)  # Mostrar 5 clientes por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'clientes': page_obj,
        'query': query,
    }
    return render(request, 'clientes/clientes_list.html', context)


def buscar_clientes_api(request):
    query = request.GET.get('q', '')
    clientes = ClienteProfile.objects.filter(
        Q(razon_social__icontains=query) |
        Q(ruc__icontains=query) |
        Q(persona_contacto__icontains=query) |
        Q(correo_contacto__icontains=query)
    ).values(
        'pk', 
        'razon_social', 
        'ruc', 
        'persona_contacto', 
        'correo_contacto', 
        'creado_en'
    )[:10] # Limitar a 10 resultados para que el autocompletado sea rápido

    # Convertir la fecha a un formato legible antes de devolver JSON
    for cliente in clientes:
        cliente['creado_en'] = cliente['creado_en'].strftime("%d %b %Y")

    return JsonResponse(list(clientes), safe=False)

@login_required
def crear_editar_cliente(request, pk=None):
    cliente = None
    if pk:
        cliente = get_object_or_404(ClienteProfile, pk=pk, user=request.user)

    errors = {}  # Dictionary to hold errors

    if request.method == 'POST':
        # Validar si el RUC ya existe para un cliente diferente
        ruc = request.POST.get('ruc')
        if ClienteProfile.objects.filter(ruc=ruc).exclude(pk=pk).exists():
            errors['ruc'] = 'Ya existe un cliente con este número de RUC.'

        if not errors:
            try:
                if cliente:
                    # Lógica de edición
                    cliente.razon_social = request.POST.get('razon_social')
                    cliente.ruc = ruc
                    cliente.direccion = request.POST.get('direccion')
                    cliente.persona_contacto = request.POST.get('persona_contacto')
                    cliente.cargo_contacto = request.POST.get('cargo_contacto')
                    cliente.celular_contacto = request.POST.get('celular_contacto')
                    cliente.correo_contacto = request.POST.get('correo_contacto')
                    
                    if 'firma_electronica' in request.FILES:
                        cliente.firma_electronica = request.FILES['firma_electronica']
                    
                    cliente.save()
                else:
                    # Lógica de creación
                    ClienteProfile.objects.create(
                        user=request.user, # Asigna el usuario
                        razon_social=request.POST.get('razon_social'),
                        ruc=ruc,
                        direccion=request.POST.get('direccion'),
                        persona_contacto=request.POST.get('persona_contacto'),
                        cargo_contacto=request.POST.get('cargo_contacto'),
                        celular_contacto=request.POST.get('celular_contacto'),
                        correo_contacto=request.POST.get('correo_contacto'),
                        firma_electronica=request.FILES.get('firma_electronica')
                    )
                return redirect('clientes:lista_clientes')
            except IntegrityError:
                # Esto es un fallback, la validación del RUC debería manejarlo.
                errors['ruc'] = 'Error al guardar. El RUC podría ya existir.'

    context = {
        'cliente': cliente,
        'errors': errors,
    }
    return render(request, 'clientes/clientes_form.html', context)

@login_required
def confirmar_eliminar_cliente(request, pk):
    cliente = get_object_or_404(ClienteProfile, pk=pk, user=request.user)
    if request.method == 'POST':
        cliente.delete()
        return redirect('lista_clientes')
    return render(request, 'clientes/clientes_confirm_delete.html', {'cliente': cliente})