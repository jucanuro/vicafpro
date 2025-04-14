from django.shortcuts import render, get_object_or_404, redirect
from .models import Postulacion, OportunidadTrabajo
from .forms import PostulacionForm

# Vista para mostrar la lista de postulaciones
def lista_postulaciones(request):
    postulaciones = Postulacion.objects.all().order_by('-creado')
    return render(request, 'bolsa_trabajo/lista_postulaciones.html', {'postulaciones': postulaciones})

# Vista para crear una nueva postulación
def crear_postulacion(request):
    if request.method == 'POST':
        form = PostulacionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_postulaciones')
    else:
        form = PostulacionForm()
    return render(request, 'bolsa_trabajo/crear_postulacion.html', {'form': form})

# Vista para ver los detalles de una postulación
def detalle_postulacion(request, id):
    postulacion = get_object_or_404(Postulacion, id=id)
    return render(request, 'bolsa_trabajo/detalle_postulacion.html', {'postulacion': postulacion})

def lista_oportunidades(request):
    oportunidades = OportunidadTrabajo.objects.filter(activo=True).order_by('-creado')
    return render(request, 'bolsa_trabajo/lista_oportunidades.html', {'oportunidades': oportunidades})

# Vista para crear una nueva oportunidad de trabajo
def crear_oportunidad(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        archivo_bases = request.FILES.get('archivo_bases')
        descripcion = request.POST.get('descripcion')
        estado = request.POST.get('estado')
        activo = request.POST.get('activo') == 'on'

        OportunidadTrabajo.objects.create(
            titulo=titulo,
            archivo_bases=archivo_bases,
            descripcion=descripcion,
            estado=estado,
            activo=activo
        )
        return redirect('lista_oportunidades')

    return render(request, 'bolsa_trabajo/crear_oportunidad.html')

# Vista para ver los detalles de una oportunidad de trabajo
def detalle_oportunidad(request, id):
    oportunidad = get_object_or_404(OportunidadTrabajo, id=id)
    return render(request, 'bolsa_trabajo/detalle_oportunidad.html', {'oportunidad': oportunidad})
