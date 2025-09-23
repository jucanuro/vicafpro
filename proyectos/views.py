from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from django.db import IntegrityError
from django.utils import timezone
from .models import Proyecto
from clientes.models import ClienteProfile
from servicios.models import Cotizacion

@login_required
def lista_proyectos(request):
    """
    Muestra la lista de proyectos con búsqueda y paginación.
    Permite filtrar por proyectos pendientes de registro de muestras.
    """
    query = request.GET.get('q')
    estado_filtro = request.GET.get('estado')

    # Obtenemos todos los proyectos y los ordenamos por fecha
    proyectos_list = Proyecto.objects.all().order_by('-creado_en')
    
    if query:
        proyectos_list = proyectos_list.filter(
            Q(nombre_proyecto__icontains=query) |
            Q(cliente__razon_social__icontains=query)
        )
    
    if estado_filtro:
        proyectos_list = proyectos_list.filter(estado=estado_filtro)

    # Añadimos la información de la cotización a cada proyecto
    proyectos_con_cotizacion = []
    for proyecto in proyectos_list:
        cotizacion = proyecto.cotizacion
        if cotizacion:
            proyecto.monto_total = cotizacion.monto_total
            # Asumimos que el modelo Voucher tiene un campo para el número de voucher
            proyecto.numero_voucher = cotizacion.voucher.codigo if hasattr(cotizacion, 'voucher') else 'N/A'
        else:
            proyecto.monto_total = 'N/A'
            proyecto.numero_voucher = 'N/A'
        proyectos_con_cotizacion.append(proyecto)

    paginator = Paginator(proyectos_con_cotizacion, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'proyectos': page_obj,
        'query': query,
        # Pasamos los estados del modelo para el filtro en el template
        'estados': Proyecto.ESTADO_PROYECTO,
        'estado_seleccionado': estado_filtro,
    }
    return render(request, 'proyectos/proyectos_list.html', context)

@login_required
def crear_proyecto(request):
    """
    Crea un nuevo proyecto.
    """
    clientes = Cliente.objects.all()
    cotizaciones = Cotizacion.objects.all()
    if request.method == 'POST':
        nombre = request.POST.get('nombre_proyecto')
        cliente_id = request.POST.get('cliente')
        cotizacion_id = request.POST.get('cotizacion')
        
        cliente = get_object_or_404(Cliente, pk=cliente_id)
        cotizacion = get_object_or_404(Cotizacion, pk=cotizacion_id) if cotizacion_id else None

        Proyecto.objects.create(
            nombre_proyecto=nombre,
            cliente=cliente,
            cotizacion_relacionada=cotizacion
        )
        return redirect('proyectos:lista_proyectos')

    context = {
        'clientes': clientes,
        'cotizaciones': cotizaciones
    }
    return render(request, 'proyectos/proyecos_form.html', context)

@login_required
def editar_proyecto(request, pk):
    """
    Edita un proyecto existente.
    """
    proyecto = get_object_or_404(Proyecto, pk=pk)
    clientes = Cliente.objects.all()
    cotizaciones = Cotizacion.objects.all()
    if request.method == 'POST':
        proyecto.nombre_proyecto = request.POST.get('nombre_proyecto')
        proyecto.cliente = get_object_or_404(Cliente, pk=request.POST.get('cliente'))
        cotizacion_id = request.POST.get('cotizacion')
        proyecto.cotizacion_relacionada = get_object_or_404(Cotizacion, pk=cotizacion_id) if cotizacion_id else None
        
        proyecto.save()
        return redirect('proyectos:lista_proyectos')
    
    context = {
        'proyecto': proyecto,
        'clientes': clientes,
        'cotizaciones': cotizaciones
    }
    return render(request, 'proyectos/proyectos_form.html', context)

@login_required
def eliminar_proyecto(request, pk):
    """
    Elimina un proyecto.
    """
    proyecto = get_object_or_404(Proyecto, pk=pk)
    if request.method == 'POST':
        proyecto.delete()
        return redirect('proyectos:lista_proyectos')
    
    context = {'proyecto': proyecto}
    return render(request, 'proyectos/eliminar_proyecto.html', context)

def lista_proyectos_pendientes(request):
    proyectos_pendientes = Proyecto.objects.filter(estado='PENDIENTE')
    context = {
        'proyectos_pendientes': proyectos_pendientes,
    }
    return render(request, 'proyectos/lista_proyectos_pendientes.html', context)


@csrf_exempt
def editar_proyecto_view(request, pk):
    """
    Vista para editar un proyecto existente.
    Maneja las solicitudes POST desde el modal de edición.
    """
    if request.method == 'POST':
        try:
            # Obtener el proyecto por su clave primaria (pk) o devolver un 404
            proyecto = get_object_or_404(Proyecto, pk=pk)
            
            # Decodificar el cuerpo JSON de la solicitud
            data = json.loads(request.body)
            
            # Actualizar los campos del proyecto con los nuevos datos
            proyecto.nombre_proyecto = data.get('nombre', proyecto.nombre_proyecto)
            proyecto.estado = data.get('estado', proyecto.estado)
            proyecto.monto_cotizacion = data.get('monto', proyecto.monto_cotizacion)
            
            # Guardar los cambios en la base de datos
            proyecto.save()
            
            # Devolver una respuesta JSON de éxito
            return JsonResponse({'success': True, 'message': 'Proyecto actualizado con éxito.'})
            
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Formato JSON inválido.'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    
    # Si la solicitud no es POST, devolver un error o renderizar una plantilla
    return JsonResponse({'success': False, 'message': 'Método no permitido.'}, status=405)



@require_POST
def create_and_edit_muestra(request):
    """
    Crea o edita una muestra para un proyecto específico.
    La lógica se ha actualizado para que una OrdenDeEnsayo pueda
    contener múltiples muestras.
    """
    try:
        data = json.loads(request.body)
        proyecto_id = data.get('proyecto_id')
        muestra_id = data.get('muestra_id')
        
        # 1. Obtener el proyecto o devolver un error si no existe
        proyecto = get_object_or_404(Proyecto, pk=proyecto_id)
        
        # 2. Encontrar o crear la OrdenDeEnsayo para este proyecto.
        # Esto asegura que todas las muestras del mismo proyecto estén ligadas a una única orden.
        orden_ensayo, created = OrdenDeEnsayo.objects.get_or_create(
            proyecto=proyecto,
            defaults={'nombre_orden': f"Orden para Proyecto {proyecto.nombre_proyecto}"}
        )

        # 3. Preparar los datos de la muestra
        muestra_data = {
            'orden': orden_ensayo,
            'codigo_muestra': data.get('codigo_muestra'),
            'descripcion_muestra': data.get('descripcion_muestra'),
            'id_lab': data.get('id_lab'),
            'tipo_muestra': data.get('tipo_muestra'),
            'masa_aprox_kg': data.get('masa_aprox_kg'),
            'fecha_recepcion': data.get('fecha_recepcion'),
            'fecha_fabricacion': data.get('fecha_fabricacion'),
            'fecha_ensayo_rotura': data.get('fecha_ensayo_rotura'),
            'informe': data.get('informe'),
            'fecha_informe': data.get('fecha_informe'),
            'estado': data.get('estado'),
            'ensayos_a_realizar': data.get('ensayos_a_realizar'),
        }

        if muestra_id:
            # Lógica para editar una muestra existente
            muestra = get_object_or_404(Muestra, pk=muestra_id)
            for key, value in muestra_data.items():
                setattr(muestra, key, value)
            muestra.save()
            message = "Muestra actualizada con éxito."
        else:
            # Lógica para crear una nueva muestra
            muestra = Muestra.objects.create(**muestra_data)
            message = "Muestra registrada con éxito."

        response_data = {
            'status': 'success',
            'message': message,
            'muestra': {
                'id': muestra.pk,
                'codigo_muestra': muestra.codigo_muestra,
                'descripcion_muestra': muestra.descripcion_muestra,
                'fecha_recepcion': muestra.fecha_recepcion.strftime('%Y-%m-%d'),
                'id_lab': muestra.id_lab,
                'tipo_muestra': muestra.tipo_muestra,
            }
        }
        return JsonResponse(response_data)

    except Proyecto.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Proyecto no encontrado.'}, status=404)
    except IntegrityError:
        return JsonResponse({'status': 'error', 'message': 'Ya existe una muestra con este código en la base de datos.'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@require_GET
def muestras_del_proyecto(request, proyecto_id):
    """
    Devuelve la lista de muestras para un proyecto específico en formato JSON.
    """
    try:
        # Busca todas las OrdenesDeEnsayo para el proyecto
        ordenes = OrdenDeEnsayo.objects.filter(proyecto_id=proyecto_id)
        # Obtiene todas las muestras de esas órdenes
        muestras = Muestra.objects.filter(orden__in=ordenes).order_by('-creado_en')
        
        muestras_list = [
            {
                'id': muestra.pk,
                'codigo_muestra': muestra.codigo_muestra,
                'descripcion_muestra': muestra.descripcion_muestra,
                'fecha_recepcion': muestra.fecha_recepcion.strftime('%Y-%m-%d'),
            }
            for muestra in muestras
        ]
        
        return JsonResponse({'status': 'success', 'muestras': muestras_list})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    """
    Devuelve la lista de muestras para un proyecto específico en formato JSON.

    Args:
        request (HttpRequest): La petición GET.
        proyecto_id (int): El ID del proyecto.
    
    Returns:
        JsonResponse: Un JSON con la lista de muestras del proyecto.
    """
    try:
        # Busca todas las OrdenesDeEnsayo para el proyecto
        ordenes = OrdenDeEnsayo.objects.filter(proyecto_id=proyecto_id)
        # Obtiene todas las muestras de esas órdenes
        muestras = Muestra.objects.filter(orden__in=ordenes).order_by('-creado_en')
        
        muestras_list = [
            {
                'id': muestra.pk,
                'codigo_muestra': muestra.codigo_muestra,
                'descripcion_muestra': muestra.descripcion_muestra,
                'fecha_recepcion': muestra.fecha_recepcion.strftime('%Y-%m-%d'),
            }
            for muestra in muestras
        ]
        
        return JsonResponse({'status': 'success', 'muestras': muestras_list})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)