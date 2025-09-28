from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from django.db import IntegrityError, transaction
from django.utils import timezone
from .models import Proyecto, OrdenDeEnsayo, Muestra    
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


@login_required
# Mantenemos el nombre de la función que ya usas
def lista_proyectos_pendientes(request): 
    """
    Vista modificada para cargar TODOS los proyectos sin importar su estado 
    (PENDIENTE, EN CURSO, FINALIZADO, etc.).
    """
    
    # 🟢 CORRECCIÓN CLAVE: Usar .all() para recuperar todos los proyectos
    proyectos = Proyecto.objects.all().order_by('-creado_en')
    
    context = {
        # 🟢 CAMBIO CLAVE: Renombramos la variable del contexto para que 
        # coincida con el nombre que usa tu template (proyectos_pendientes)
        'proyectos_pendientes': proyectos, 
        'titulo_lista': 'Todos los Proyectos para Gestión', 
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
            proyecto = get_object_or_404(Proyecto, pk=pk)
            data = json.loads(request.body)
            proyecto.nombre_proyecto = data.get('nombre', proyecto.nombre_proyecto)
            proyecto.estado = data.get('estado', proyecto.estado)
            proyecto.monto_cotizacion = data.get('monto', proyecto.monto_cotizacion)
            proyecto.save()
            return JsonResponse({'success': True, 'message': 'Proyecto actualizado con éxito.'})
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Formato JSON inválido.'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    return JsonResponse({'success': False, 'message': 'Método no permitido.'}, status=405)



@csrf_exempt
def create_and_edit_muestra(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            proyecto_id = data.get('proyecto_id')
            # ... (otras variables de data) ...
            
            # --- Validaciones y Obtención del Proyecto ---
            if not proyecto_id:
                return JsonResponse({'status': 'error', 'message': 'El ID del proyecto no puede ser nulo.'}, status=400)

            try:
                proyecto = Proyecto.objects.get(id=proyecto_id)
            except Proyecto.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'El proyecto no existe.'}, status=404)

            # Evitar duplicidad: verificar si la muestra ya existe para este proyecto
            codigo_muestra = data.get('codigo_muestra')
            if Muestra.objects.filter(proyecto=proyecto, codigo_muestra=codigo_muestra).exists():
                return JsonResponse({'status': 'error', 'message': f'Ya existe una muestra con el código "{codigo_muestra}" para este proyecto.'}, status=400)

            # Usamos una transacción para asegurar que todas las operaciones se completen o se reviertan
            with transaction.atomic():
                # --- Creación de Muestra ---
                muestra = Muestra.objects.create(
                    proyecto=proyecto,
                    codigo_muestra=codigo_muestra,
                    descripcion_muestra=data.get('descripcion_muestra'),
                    id_lab=data.get('id_lab'),
                    tipo_muestra=data.get('tipo_muestra'),
                    masa_aprox_kg=data.get('masa_aprox_kg'),
                    fecha_recepcion=data.get('fecha_recepcion'),
                    fecha_fabricacion=data.get('fecha_fabricacion'),
                    fecha_ensayo_rotura=data.get('fecha_ensayo_rotura'),
                    informe=data.get('informe'),
                    fecha_informe=data.get('fecha_informe'),
                    estado=data.get('estado', Muestra.ESTADOS_MUESTRA[0][0]),
                    ensayos_a_realizar=data.get('ensayos_a_realizar')
                )
                
                # --- Creación de Orden de Ensayo (vinculada a la Muestra) ---
                orden_ensayo = OrdenDeEnsayo.objects.create(
                    muestra=muestra,
                    proyecto=proyecto,
                    tipo_ensayo="Ensayo de " + data.get('tipo_muestra', 'Muestra Genérica'),
                    # Asegurarse de que la fecha_entrega_programada sea un campo válido o se use una lógica real
                    fecha_entrega_programada=timezone.now().date()
                )

                # --- LÓGICA DE ACTUALIZACIÓN DEL PROYECTO ---
                # 1. Incrementar el contador de muestras
                proyecto.numero_muestras_registradas = Proyecto.objects.filter(id=proyecto_id).first().muestras.count() + 1
                
                # 2. Cambiar estado a 'EN_CURSO' si estaba 'PENDIENTE'
                if proyecto.estado == 'PENDIENTE':
                    proyecto.estado = 'EN_CURSO' # El estado ahora es 'EN_CURSO'
                
                proyecto.save()
                # -------------------------------------------
            
            return JsonResponse({
                'status': 'success',
                'message': 'Muestra y Orden de Ensayo creadas correctamente.',
                'muestra': {
                    'codigo_muestra': muestra.codigo_muestra,
                    'tipo_muestra': muestra.tipo_muestra,
                    'estado': muestra.estado,
                    'orden_ensayo_id': orden_ensayo.id # Devolvemos el ID de la Orden de Ensayo
                }
            }, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'JSON inválido.'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Método de solicitud no permitido.'}, status=405)



@require_GET
def muestras_del_proyecto(request, proyecto_id):
    """
    Devuelve la lista de muestras para un proyecto específico en formato JSON,
    incluyendo la ID de la Orden de Ensayo para facilitar el acceso al formulario.
    """
    try:
        # Usamos select_related para obtener la OrdenDeEnsayo de manera eficiente
        muestras = Muestra.objects.filter(proyecto_id=proyecto_id).order_by('-creado_en').prefetch_related('ordenes')
        
        muestras_list = [
            {
                'id': muestra.pk,
                'codigo_muestra': muestra.codigo_muestra,
                'descripcion_muestra': muestra.descripcion_muestra,
                'fecha_recepcion': muestra.fecha_recepcion.strftime('%Y-%m-%d'),
                'estado': muestra.get_estado_display(), # Usamos get_estado_display para el texto amigable
                # Buscamos la primera OrdenDeEnsayo vinculada a esta muestra
                'orden_ensayo_id': muestra.ordenes.first().id if muestra.ordenes.exists() else None, 
            }
            for muestra in muestras
        ]
        
        # Opcional: Obtener el estado actual del proyecto para el frontend
        proyecto = Proyecto.objects.get(id=proyecto_id)

        return JsonResponse({
            'status': 'success', 
            'muestras': muestras_list,
            'proyecto_estado': proyecto.get_estado_display()
        })
        
    except Proyecto.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'El proyecto no existe.'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
def orden_de_ensayo_form(request, orden_id):
    # 'orden_id' debe coincidir con lo que definiste en la URL
    from .models import OrdenDeEnsayo 
    orden = get_object_or_404(OrdenDeEnsayo, pk=orden_id)
    
    # ... tu lógica aquí ...
    return render(request, 'proyectos/orden_ensayo_form.html', {'orden': orden})
  
    
@login_required
def orden_de_ensayo_documento(request, pk):
    """
    Vista para visualizar el Documento/Ficha de la Orden de Ensayo.
    Muestra al técnico las características de la muestra y los ensayos a realizar.
    """
    # Usamos 'pk' para OrdenDeEnsayo
    orden = get_object_or_404(OrdenDeEnsayo, pk=pk)
    
    muestra = orden.muestra
    proyecto = orden.proyecto
    
    # **Acción Clave:** Si la orden está pendiente, la marcamos como 'EN_PROCESO' para el técnico.
    if orden.estado_orden == 'PENDIENTE':
        orden.estado_orden = 'EN_PROCESO'
        orden.save()
        
    # El técnico necesita saber si ya existen resultados para esta muestra
    # La lógica para obtener el último resultado es correcta
    try:
        resultado_actual = muestra.resultados.latest('creado_en') 
    except ResultadoEnsayo.DoesNotExist:
        resultado_actual = None 

    context = {
        'orden': orden,
        'muestra': muestra,
        'proyecto': proyecto,
        'resultado_actual': resultado_actual, # Usado para saber si hay resultados
    }
    # Renderizamos un template que actúa como un documento de ficha técnica
    return render(request, 'proyectos/orden_ensayo_documento.html', context)


@login_required
def registro_resultado_form(request, muestra_pk):
    """
    Vista para el formulario de ingreso de datos para una Muestra específica.
    """
    # 1. Obtenemos la muestra por su PK
    muestra = get_object_or_404(Muestra, pk=muestra_pk)
    
    # 2. Obtenemos la orden de ensayo relacionada
    # Asumimos que la muestra tiene una orden, si no, habría un error lógico previo
    orden = muestra.ordenes.first() 
    
    # 3. Lógica para manejar el formulario (POST)
    if request.method == 'POST':
        # Aquí va la lógica de Formulario/Formset para crear o actualizar ResultadoEnsayo
        
        # Una vez guardado, se debe actualizar el estado de la Orden de Ensayo
        if orden:
            orden.estado_orden = 'RESULTADOS_REGISTRADOS'
            orden.save()
        
        # return redirect('alguna_vista_de_exito') 
        pass

    context = {
        'muestra': muestra,
        'orden': orden,
        # Aquí pasarías el formulario de resultados
    }
    return render(request, 'proyectos/registro_resultado_form.html', context)