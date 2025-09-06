from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.http import JsonResponse, HttpResponse
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import json
from decimal import Decimal
from django.db.models import Q

from .models import Servicio, DetalleServicio, Cotizacion, Norma, Metodo, Voucher, CotizacionDetalle
from clientes.models import ClienteProfile
from .forms import ServicioForm, DetalleServicioForm, CotizacionForm

DetalleServicioFormSet = inlineformset_factory(
    Servicio,
    DetalleServicio,
    form=DetalleServicioForm,
    extra=1,
    can_delete=True
)

def servicios_view(request):
    return render(request, 'servicios/servicios.html')

def detalle_servicios_view(request):
    return render(request, 'servicios/detalleservicios.html')

class ServicioListView(LoginRequiredMixin, ListView):
    model = Servicio
    template_name = 'servicios/servicio_list.html'
    context_object_name = 'servicios'
    ordering = ['orden']
    
class ServicioDetailView(LoginRequiredMixin, DetailView):
    model = Servicio
    template_name = 'servicios/servicio_detail.html'
    context_object_name = 'servicio'

class ServicioDeleteView(LoginRequiredMixin, DeleteView):
    model = Servicio
    template_name = 'servicios/servicio_confirm_delete.html'
    success_url = reverse_lazy('servicios:servicio_list')

@login_required
def servicio_create_or_update(request, pk=None):
    servicio = get_object_or_404(Servicio, pk=pk) if pk else None
    form = ServicioForm(request.POST or None, request.FILES or None, instance=servicio)
    formset = DetalleServicioFormSet(request.POST or None, request.FILES or None, instance=servicio)
    if request.method == 'POST':
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                servicio = form.save()
                formset.instance = servicio
                formset.save()
            return redirect('servicios:servicio_list')
    context = {
        'form': form,
        'formset': formset,
        'servicio': servicio
    }
    return render(request, 'servicios/servicio_form.html', context)

def buscar_cliente(request):
    query = request.GET.get('q', '')
    clientes = []
    if query:
        clientes = ClienteProfile.objects.filter(
            Q(razon_social__icontains=query) | Q(ruc__icontains=query)
        ).values('id', 'razon_social', 'ruc', 'persona_contacto', 'correo_contacto', 'telefono_contacto')[:10]
    return JsonResponse(list(clientes), safe=False)

def buscar_servicio(request):
    query = request.GET.get('q', '')
    servicios = []
    if query:
        servicios = Servicio.objects.filter(nombre__icontains=query).values('id', 'nombre')[:10]
    return JsonResponse(list(servicios), safe=False)

def obtener_detalles_servicio(request, servicio_id):
    servicio = get_object_or_404(Servicio, pk=servicio_id)
    normas = list(servicio.normas.all().values('id', 'nombre'))
    metodos = list(servicio.metodos.all().values('id', 'nombre'))
    detalles = list(servicio.detalles.all().values('id', 'titulo'))
    return JsonResponse({'normas': normas, 'metodos': metodos, 'detalles': detalles})

@csrf_protect
@login_required
def crear_cotizacion(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            cliente = get_object_or_404(ClienteProfile, pk=data['cliente_id'])
            with transaction.atomic():
                cotizacion = Cotizacion.objects.create(
                    cliente=cliente,
                    numero_oferta=data['numero_oferta'],
                    persona_contacto=data['persona_contacto'],
                    correo_contacto=data['correo_contacto'],
                    telefono_contacto=data['telefono_contacto'],
                    forma_pago=data['forma_pago'],
                    validez_oferta_dias=data['validez_oferta_dias'],
                    plazo_entrega_dias=data['plazo_entrega_dias'],
                    monto_total=Decimal(str(data['monto_total'])),
                    estado='Pendiente'
                )
                for item_data in data['detalles']:
                    servicio = get_object_or_404(Servicio, pk=item_data['servicio_id'])
                    detalle_servicio = get_object_or_404(DetalleServicio, pk=item_data['detalle_servicio_id'])
                    CotizacionDetalle.objects.create(
                        cotizacion=cotizacion,
                        servicio=servicio,
                        detalle_servicio=detalle_servicio,
                        und=item_data['und'],
                        cantidad=int(item_data['cantidad']),
                        precio_unitario=Decimal(str(item_data['precio_unitario']))
                    )
            return JsonResponse({'message': 'Cotización creada y guardada con éxito', 'numero_oferta': cotizacion.numero_oferta})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return HttpResponse(status=405)

def ver_cotizacion(request, numero_oferta):
    cotizacion = get_object_or_404(Cotizacion, numero_oferta=numero_oferta)
    return render(request, 'servicios/cotizacion_cliente.html', {'cotizacion': cotizacion})

def aceptar_cotizacion(request, cotizacion_id):
    cotizacion = get_object_or_404(Cotizacion, pk=cotizacion_id)
    if request.method == 'POST':
        cotizacion.estado = 'Aceptada'
        cotizacion.save()
        return JsonResponse({'message': 'Cotización aceptada con éxito'})
    return HttpResponse(status=405)

def rechazar_cotizacion(request, cotizacion_id):
    cotizacion = get_object_or_404(Cotizacion, pk=cotizacion_id)
    if request.method == 'POST':
        cotizacion.estado = 'Rechazada'
        cotizacion.save()
        return JsonResponse({'message': 'Cotización rechazada con éxito'})
    return HttpResponse(status=405)

@csrf_protect
def subir_voucher(request, cotizacion_id):
    cotizacion = get_object_or_404(Cotizacion, pk=cotizacion_id)
    if request.method == 'POST':
        try:
            codigo = request.POST.get('codigo_voucher')
            imagen = request.FILES.get('imagen_voucher')
            if not codigo or not imagen:
                return JsonResponse({'error': 'Código de voucher e imagen son requeridos.'}, status=400)
            Voucher.objects.create(
                cotizacion=cotizacion,
                codigo=codigo,
                imagen=imagen
            )
            return JsonResponse({'message': 'Voucher subido con éxito.'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return HttpResponse(status=405)

class CotizacionListView(LoginRequiredMixin, ListView):
    model = Cotizacion
    template_name = 'cotizacion_list.html'
    context_object_name = 'cotizaciones'
    ordering = ['-fecha_creacion']