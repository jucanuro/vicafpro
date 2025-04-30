from django.shortcuts import render, get_object_or_404, redirect
from .models import OportunidadTrabajo
from .forms import PostulacionForm

def lista_oportunidades(request):
    oportunidades = OportunidadTrabajo.objects.filter(activo=True, estado='publicado')
    return render(request, 'index.html', {'oportunidades': oportunidades})

def postular(request, oportunidad_id): 
    oportunidad = get_object_or_404(Oportunidad, pk=oportunidad_id)

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
   
    return render(request, 'bolsa_trabajo/postular_form.html', context)
