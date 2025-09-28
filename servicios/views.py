# servicios/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
import json
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.db.models import Sum
from django.db import transaction 
from django.contrib.auth.decorators import login_required
from weasyprint import HTML
from django.http import HttpResponse
from django.template.loader import get_template
from decimal import Decimal
from proyectos.models import Proyecto
from .models import Servicio, Norma, Metodo, DetalleServicio,Cotizacion, CotizacionDetalle, ClienteProfile,Voucher
from .forms import ServicioForm # Asumiendo que crearás este formulario




# ---------------------------------------------------------------
# Nuevas vistas agregadas
# ---------------------------------------------------------------

def servicios_view(request):
    """
    Vista principal para mostrar los servicios del sitio web.
    """
    return render(request, 'servicios/servicios.html')

def detalle_servicios_view(request):
    """
    Vista para mostrar el detalle de un servicio del sitio web.
    """
    return render(request, 'servicios/detalleservicios.html')


# ---------------------------------------------------------------
# Vistas para la gestión de Servicios (CRUD)
# ---------------------------------------------------------------

def lista_servicios(request):
    """
    Muestra una lista de todos los servicios con paginación y búsqueda.
    """
    query = request.GET.get('q')
    if query:
        servicios_list = Servicio.objects.filter(
            Q(nombre__icontains=query) | Q(descripcion__icontains=query)
        ).order_by('orden')
    else:
        servicios_list = Servicio.objects.all().order_by('orden')

    paginator = Paginator(servicios_list, 10) # 10 servicios por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'servicios': page_obj,
        'query': query,
    }
    return render(request, 'servicios/servicios_list.html', context)

def obtener_detalle_servicio_api(request, pk):
    """
    Devuelve los detalles de un servicio en formato JSON para uso en el modal.
    """
    servicio = get_object_or_404(Servicio, pk=pk)
    detalle = getattr(servicio, 'detalleservicio', None)
    
    data = {
        'nombre': servicio.nombre,
        'descripcion': servicio.descripcion,
        'orden': servicio.orden,
        'imagen_url': servicio.imagen.url if servicio.imagen else None,
        'normas': [norma.nombre for norma in servicio.normas.all()],
        'metodos': [metodo.nombre for metodo in servicio.metodos.all()],
        'detalle': {
            'titulo': detalle.titulo,
            'descripcion': detalle.descripcion,
            'imagen_url': detalle.imagen.url if detalle.imagen else None,
        } if detalle else None
    }
    return JsonResponse(data)

def crear_servicio(request):
    """
    Crea un nuevo servicio, su detalle y asocia las normas y métodos.
    """
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        orden = request.POST.get('orden', 0)
        imagen = request.FILES.get('imagen')
        
        # Validación básica para campos no vacíos
        if not nombre or not descripcion:
            return render(request, 'servicios/servicios_form.html', {
                'servicio': None,
                'error': 'El nombre y la descripción son campos obligatorios.'
            })

        try:
            servicio_guardado = Servicio.objects.create(
                nombre=nombre,
                descripcion=descripcion,
                orden=orden,
                imagen=imagen
            )

            # Guardar el Detalle del Servicio
            detalle_titulo = request.POST.get('detalle_titulo')
            detalle_descripcion = request.POST.get('detalle_descripcion')
            detalle_imagen = request.FILES.get('detalle_imagen')

            if detalle_titulo or detalle_descripcion or detalle_imagen:
                DetalleServicio.objects.create(
                    servicio=servicio_guardado,
                    titulo=detalle_titulo,
                    descripcion=detalle_descripcion,
                    imagen=detalle_imagen
                )

            # Asociar Normas y Métodos existentes o crear nuevos
            normas_data = request.POST.getlist('normas')
            metodos_data = request.POST.getlist('metodos')

            for nombre_norma in normas_data:
                if nombre_norma:
                    norma, created = Norma.objects.get_or_create(nombre=nombre_norma)
                    servicio_guardado.normas.add(norma)

            for nombre_metodo in metodos_data:
                if nombre_metodo:
                    metodo, created = Metodo.objects.get_or_create(nombre=nombre_metodo)
                    servicio_guardado.metodos.add(metodo)

            return redirect('servicios:lista_servicios')

        except Exception as e:
            return render(request, 'servicios/servicios_form.html', {
                'servicio': None,
                'error': f'Ocurrió un error al guardar el servicio: {e}'
            })

    return render(request, 'servicios/servicios_form.html', {'servicio': None})


def editar_servicio(request, pk):
    """
    Edita un servicio existente y sus elementos asociados, cargando la información
    existente en el formulario.
    """
    servicio = get_object_or_404(Servicio, pk=pk)
    
    # Intenta obtener el detalle del servicio para pasarlo a la plantilla.
    # Si no existe, 'detalle' será None.
    detalle = getattr(servicio, 'detalleservicio', None)

    if request.method == 'POST':
        # --- LÓGICA DE GUARDADO (POST) ---
        # (Esta parte ya estaba bien, la mantengo para referencia)
        servicio.nombre = request.POST.get('nombre')
        servicio.descripcion = request.POST.get('descripcion')
        servicio.orden = request.POST.get('orden', 0)
        
        imagen_nueva = request.FILES.get('imagen')
        if imagen_nueva:
            servicio.imagen = imagen_nueva
        
        servicio.save()

        DetalleServicio.objects.update_or_create(
            servicio=servicio,
            defaults={
                'titulo': request.POST.get('detalle_titulo'),
                'descripcion': request.POST.get('detalle_descripcion'),
                'imagen': request.FILES.get('detalle_imagen') if request.FILES.get('detalle_imagen') else detalle.imagen if detalle else None
            }
        )

        servicio.normas.clear()
        servicio.metodos.clear()

        normas_data = request.POST.getlist('normas')
        metodos_data = request.POST.getlist('metodos')

        for nombre_norma in normas_data:
            if nombre_norma:
                norma, _ = Norma.objects.get_or_create(nombre=nombre_norma)
                servicio.normas.add(norma)

        for nombre_metodo in metodos_data:
            if nombre_metodo:
                metodo, _ = Metodo.objects.get_or_create(nombre=nombre_metodo)
                servicio.metodos.add(metodo)

        return redirect('servicios:lista_servicios')
    
    else:
        # --- LÓGICA DE CARGA (GET) ---
        # Aquí es donde obtenemos todos los datos para precargar el formulario.
        # Es crucial pasar estos datos a la plantilla para que se muestren.
        
        # Obtener los nombres de las normas y métodos asociados
        normas = list(servicio.normas.values_list('nombre', flat=True))
        metodos = list(servicio.metodos.values_list('nombre', flat=True))

        return render(request, 'servicios/servicios_form.html', {
            'servicio': servicio, # Objeto principal
            'detalle_servicio': detalle, # Objeto de detalle
            'normas_iniciales': normas, # Nombres de las normas
            'metodos_iniciales': metodos, # Nombres de los métodos
        })

def eliminar_servicio(request, pk):
    """
    Elimina un servicio existente.
    """
    servicio = get_object_or_404(Servicio, pk=pk)
    if request.method == 'POST':
        servicio.delete()
        return redirect('servicios:lista_servicios')

    return render(request, 'servicios/servicio_confirm_delete.html', {'servicio': servicio})


# ---------------------------------------------------------------
# Vista de API para la búsqueda en vivo
# ---------------------------------------------------------------

def buscar_servicios_api(request):
    """
    API para la búsqueda de servicios que devuelve una respuesta JSON.
    """
    query = request.GET.get('q', '')
    if query:
        servicios = Servicio.objects.filter(
            Q(nombre__icontains=query) | Q(descripcion__icontains=query)
        ).order_by('orden')
    else:
        servicios = Servicio.objects.all().order_by('orden')
    
    data = []
    for servicio in servicios:
        data.append({
            'pk': servicio.pk,
            'nombre': servicio.nombre,
            'descripcion': servicio.descripcion,
            'orden': servicio.orden,
        })
    return JsonResponse(data, safe=False)

@login_required
def lista_cotizaciones(request):
    """
    Muestra una lista de cotizaciones, filtrando por cliente si el usuario
    no es un superusuario.
    """
    query = request.GET.get('q')
    
    if request.user.is_superuser:
        cotizaciones_list = Cotizacion.objects.all().order_by('-fecha_creacion')
    else:
        # Asume que el modelo de Usuario está relacionado con el modelo de Cliente
        # Y que el cliente tiene un campo 'cotizaciones' o similar
        # Deberás adaptar esto a tu estructura de modelos
        try:
            cliente_asociado = request.user.cliente # O la forma en que relaciones a tu cliente
            cotizaciones_list = Cotizacion.objects.filter(cliente=cliente_asociado).order_by('-fecha_creacion')
        except AttributeError:
            cotizaciones_list = Cotizacion.objects.none()

    if query:
        cotizaciones_list = cotizaciones_list.filter(
            Q(numero_oferta__icontains=query) | 
            Q(cliente__razon_social__icontains=query) |
            Q(estado__icontains=query)
        ).order_by('-fecha_creacion')

    paginator = Paginator(cotizaciones_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'cotizaciones': page_obj,
        'query': query,
    }
    return render(request, 'servicios/cotizaciones_list.html', context)

def obtener_detalle_servicio_para_cotizacion_api(request, pk):
    try:
        servicio = Servicio.objects.get(pk=pk)
        
        # Obtener las normas y métodos relacionados
        normas = list(servicio.normas_relacionadas.values('id', 'nombre'))
        metodos = list(servicio.metodos_relacionados.values('id', 'nombre'))
        
        data = {
            'nombre': servicio.nombre,
            'precio_unitario': str(servicio.precio_unitario),
            'und': servicio.und,
            'normas': normas,
            'metodos': metodos,
        }
        return JsonResponse(data)
    except Servicio.DoesNotExist:
        return JsonResponse({'error': 'Servicio no encontrado'}, status=404)

def crear_cotizacion(request):
    """
    Permite crear una nueva cotización.
    """
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente')
        cliente = get_object_or_404(ClienteProfile, pk=cliente_id)

        # Genera un número de oferta automático y único
        ultima_cotizacion = Cotizacion.objects.all().order_by('-numero_oferta').first()
        if ultima_cotizacion and ultima_cotizacion.numero_oferta:
            try:
                ultimo_numero = int(ultima_cotizacion.numero_oferta.split('-')[-1])
                nuevo_numero_oferta = f'C-{ultimo_numero + 1}'
            except (ValueError, IndexError):
                nuevo_numero_oferta = 'C-1'
        else:
            nuevo_numero_oferta = 'C-1'
        
        cotizacion = Cotizacion.objects.create(
            cliente=cliente,
            numero_oferta=nuevo_numero_oferta,
            persona_contacto=request.POST.get('persona_contacto'),
            correo_contacto=request.POST.get('correo_contacto'),
            telefono_contacto=request.POST.get('telefono_contacto'),
            plazo_entrega_dias=request.POST.get('plazo_entrega_dias'),
            forma_pago=request.POST.get('forma_pago'),
            validez_oferta_dias=request.POST.get('validez_oferta_dias'),
            monto_total=Decimal(request.POST.get('monto_total')),
            estado='Pendiente',
        )

        detalles_data = json.loads(request.POST.get('detalles_json'))
        for item in detalles_data:
            servicio = get_object_or_404(Servicio, pk=item['servicio_id'])
            
            norma_id = item.get('norma_id')
            metodo_id = item.get('metodo_id')
            und = item.get('und', 'und') # Obtiene la unidad del JSON

            norma = get_object_or_404(Norma, pk=norma_id) if norma_id else None
            metodo = get_object_or_404(Metodo, pk=metodo_id) if metodo_id else None
            
            CotizacionDetalle.objects.create(
                cotizacion=cotizacion,
                servicio=servicio,
                norma=norma,
                metodo=metodo,
                und=und,
                cantidad=item['cantidad'],
                precio_unitario=item['precio_unitario'],
            )

        return redirect('servicios:lista_cotizaciones')
    
    else:
        clientes = ClienteProfile.objects.all()
        servicios = Servicio.objects.all().prefetch_related('normas', 'metodos')
        
        # Serializa los servicios con sus normas y métodos (sin la unidad)
        servicios_con_detalles_json = json.dumps([
            {
                'pk': s.pk,
                'nombre': s.nombre,
                'normas': [{'pk': n.pk, 'nombre': n.nombre} for n in s.normas.all()],
                'metodos': [{'pk': m.pk, 'nombre': m.nombre} for m in s.metodos.all()]
            } for s in servicios
        ])

        context = {
            'clientes': clientes,
            'servicios': servicios,
            'cotizacion_model': Cotizacion,
            'servicios_con_detalles_json': servicios_con_detalles_json,
        }
        return render(request, 'servicios/cotizaciones_form.html', context)


def editar_cotizacion(request, pk):
    """
    Permite editar una cotización existente y sus detalles.
    """
    cotizacion = get_object_or_404(Cotizacion, pk=pk)
    
    if request.method == 'POST':
        # Lógica para procesar la edición del formulario
        cotizacion.cliente = get_object_or_404(ClienteProfile, pk=request.POST.get('cliente'))
        cotizacion.persona_contacto = request.POST.get('persona_contacto')
        cotizacion.correo_contacto = request.POST.get('correo_contacto')
        cotizacion.telefono_contacto = request.POST.get('telefono_contacto')
        cotizacion.plazo_entrega_dias = request.POST.get('plazo_entrega_dias')
        cotizacion.forma_pago = request.POST.get('forma_pago')
        cotizacion.validez_oferta_dias = request.POST.get('validez_oferta_dias')
        
        cotizacion.monto_total = Decimal(request.POST.get('monto_total'))
        
        cotizacion.save()
        
        cotizacion.detalles_cotizacion.all().delete()
        detalles_data = json.loads(request.POST.get('detalles_json'))
        for item in detalles_data:
            servicio = get_object_or_404(Servicio, pk=item['servicio_id'])
            norma_id = item.get('norma_id')
            metodo_id = item.get('metodo_id')
            und = item.get('und', 'und')

            norma = get_object_or_404(Norma, pk=norma_id) if norma_id else None
            metodo = get_object_or_404(Metodo, pk=metodo_id) if metodo_id else None

            CotizacionDetalle.objects.create(
                cotizacion=cotizacion,
                servicio=servicio,
                norma=norma,
                metodo=metodo,
                und=und,
                cantidad=item['cantidad'],
                precio_unitario=item['precio_unitario'],
            )
        
        return redirect('servicios:lista_cotizaciones')

    else:
        clientes = ClienteProfile.objects.all()
        servicios = Servicio.objects.all().prefetch_related('normas', 'metodos')
        
        # Serializa los servicios con sus normas y métodos (sin la unidad)
        servicios_con_detalles_json = json.dumps([
            {
                'pk': s.pk,
                'nombre': s.nombre,
                'normas': [{'pk': n.pk, 'nombre': n.nombre} for n in s.normas.all()],
                'metodos': [{'pk': m.pk, 'nombre': m.nombre} for m in s.metodos.all()]
            } for s in servicios
        ])

        # Serializa los detalles de cotización (incluyendo la unidad)
        detalles_cotizacion_json = json.dumps([
            {
                'servicio_id': detalle.servicio.pk,
                'norma_id': detalle.norma.pk if detalle.norma else None,
                'metodo_id': detalle.metodo.pk if detalle.metodo else None,
                'und': detalle.und,
                'cantidad': str(detalle.cantidad),
                'precio_unitario': str(detalle.precio_unitario),
            } for detalle in cotizacion.detalles_cotizacion.all()
        ])
        
        context = {
            'cotizacion': cotizacion,
            'clientes': clientes,
            'servicios': servicios,
            'cotizacion_model': Cotizacion,
            'detalles_cotizacion_json': detalles_cotizacion_json,
            'servicios_con_detalles_json': servicios_con_detalles_json,
        }
        return render(request, 'servicios/cotizaciones_form.html', context)

def eliminar_cotizacion(request, pk):
    """
    Permite eliminar una cotización.
    """
    cotizacion = get_object_or_404(Cotizacion, pk=pk)
    if request.method == 'POST':
        cotizacion.delete()
        return redirect('servicios:lista_cotizaciones')
        
    return render(request, 'servicios/cotizacion_confirm_delete.html', {'cotizacion': cotizacion})

def buscar_cotizaciones_api(request):
    """
    API para la búsqueda de cotizaciones que devuelve una respuesta JSON.
    """
    query = request.GET.get('q', '')
    cotizaciones = []
    if query:
        cotizaciones_qs = Cotizacion.objects.filter(
            Q(numero_oferta__icontains=query) | 
            Q(cliente__razon_social__icontains=query) |
            Q(estado__icontains=query)
        ).order_by('-fecha_creacion')
        
        for cotizacion in cotizaciones_qs:
            cotizaciones.append({
                'pk': cotizacion.pk,
                'numero_oferta': cotizacion.numero_oferta,
                'cliente': cotizacion.cliente.razon_social,
                'estado': cotizacion.estado,
                'fecha_creacion': cotizacion.fecha_creacion.strftime('%Y-%m-%d %H:%M'),
            })
    
    return JsonResponse(cotizaciones, safe=False)

def generar_pdf_cotizacion(request, pk):
    cotizacion = get_object_or_404(Cotizacion, pk=pk)
    
    # Cargar la plantilla HTML para el PDF
    template = get_template('servicios/cotizacion_pdf.html')
    context = {'cotizacion': cotizacion}
    html_content = template.render(context)
    
    # Generar el PDF
    response = HttpResponse(content_type='application/pdf')
    # Usar 'inline' para abrir en la misma pestaña o 'attachment' para descargar
    response['Content-Disposition'] = f'inline; filename="cotizacion_{cotizacion.numero_oferta}.pdf"'
    
    # Generar el PDF desde el HTML
    HTML(string=html_content, base_url=request.build_absolute_uri()).write_pdf(response)
    
    return response


@csrf_exempt
def aprobar_cotizacion(request, pk):
    """
    Aprueba una cotización (desde un formulario) y crea el proyecto asociado.
    """
    cotizacion = get_object_or_404(Cotizacion, pk=pk)
    
    # ... (Validaciones de Permiso y Estado) ...

    if cotizacion.estado != 'Pendiente':
        return HttpResponse("Esta cotización ya no puede ser aprobada.", status=400)

    if request.method == 'POST':
        codigo_voucher = request.POST.get('codigo_voucher')
        imagen_voucher = request.FILES.get('imagen_voucher')
        
        if not codigo_voucher or not imagen_voucher:
            context = {
                'cotizacion': cotizacion,
                'error': 'Ambos campos, el código de operación y la imagen, son requeridos.'
            }
            return render(request, 'servicios/aprobar_cotizacion.html', context)

        with transaction.atomic():
            # 1. Crear el registro del voucher
            voucher = Voucher(
                cotizacion=cotizacion,
                codigo=codigo_voucher,
                imagen=imagen_voucher
            )
            voucher.save()
            
            # 2. Actualizar el estado de la cotización
            cotizacion.estado = 'Aceptada'
            cotizacion.save()

            # 3. Preparar datos para el Proyecto
            nombre_proyecto = f"Proyecto - {cotizacion.numero_oferta}"
            
            # Generar un código único para el Proyecto (ej. P-C-1)
            # Se asume que el numero_oferta de la cotización es único.
            codigo_proyecto = f"P-{cotizacion.numero_oferta}" 
            
            # Obtener el total de muestras (suma de las cantidades de los detalles)
            total_muestras = cotizacion.detalles_cotizacion.aggregate(Sum('cantidad'))['cantidad__sum'] or 0

            # 4. Crear el nuevo proyecto
            nuevo_proyecto = Proyecto.objects.create(
                cotizacion=cotizacion,
                nombre_proyecto=nombre_proyecto,
                codigo_proyecto=codigo_proyecto, 
                cliente=cotizacion.cliente,
                estado='PENDIENTE',
                
                # 🎯 CAMPOS ADICIONALES AHORA VÁLIDOS EN EL MODELO PROYECTO
                descripcion_proyecto="Proyecto generado automáticamente a partir de una cotización aceptada.",
                monto_cotizacion=cotizacion.monto_total,
                codigo_voucher=voucher.codigo, # El código del voucher que acabamos de guardar
                numero_muestras=total_muestras, # Mapeado al campo correcto 'numero_muestras'
            )
            
            # 5. Redirigir al listado de proyectos pendientes
            return redirect('proyectos:lista_proyectos_pendientes')
    
    context = {
        'cotizacion': cotizacion
    }
    return render(request, 'servicios/aprobar_cotizacion.html', context)