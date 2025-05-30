from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages 
from .models import OportunidadTrabajo
from .forms import PostulacionForm

def lista_oportunidades(request):
    oportunidades = OportunidadTrabajo.objects.filter(activo=True, estado='publicado')
    return render(request, 'bolsa_trabajo/bolsa_trabajo.html', {'oportunidades': oportunidades})

def postular(request, oportunidad_id): 
    oportunidad = get_object_or_404(OportunidadTrabajo, pk=oportunidad_id)

    if request.method == 'POST':
        form = PostulacionForm(request.POST, request.FILES)
        if form.is_valid():
            postulacion = form.save(commit=False)
            postulacion.oportunidad = oportunidad
            postulacion.save()
            messages.success(request, f'¡Has postulado exitosamente a "{oportunidad.titulo}"!') 
            
            return redirect('bolsa_trabajo:listar') 
    else: 
        form = PostulacionForm()

    context = {
        'form': form,
        'oportunidad': oportunidad, 
    }
   
    return render(request, 'bolsa_trabajo/form_postulacion.html', context)
