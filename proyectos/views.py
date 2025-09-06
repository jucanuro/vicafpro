# proyectos/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.units import inch
from io import BytesIO
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image as ReportLabImage
)
from django.conf import settings
import os
from .models import (Proyecto,  OrdenDeEnsayo,
    Muestra,
    ResultadoEnsayo,
    DocumentoFinal
)
from .forms import (ProyectoForm, OrdenDeEnsayoForm,
    MuestraForm,
    ResultadoEnsayoForm,
    DocumentoFinalForm
)
from django.urls import reverse_lazy


def home_view(request):
    """
    Renderiza la plantilla 'proyectos-principal.html' para la página de inicio.
    """
    return render(request, 'proyectos_principal.html')

def proyectos_view(request):
    """
    Recupera todos los objetos de Proyecto de la base de datos
    y los pasa a la plantilla 'proyectos.html' para su visualización.
    """
    proyectos = Proyecto.objects.all().order_by('-creado_en')
    context = {
        'proyectos': proyectos
    }
    return render(request, 'proyectos_list.html', context)


def crear_proyecto_view(request):
    """
    Vista para crear un nuevo proyecto.
    Maneja la lógica de mostrar el formulario y guardar el proyecto.
    """
    if request.method == 'POST':
        # Si la solicitud es POST, procesa los datos del formulario
        form = ProyectoForm(request.POST)
        if form.is_valid():
            proyecto = form.save()
            # Redirecciona a la página de lista de proyectos
            return redirect('proyectos:lista_proyectos')
    else:
        # Si la solicitud es GET, muestra un formulario vacío
        form = ProyectoForm()

    context = {
        'form': form,
    }
    return render(request, 'proyectos_crear.html', context)


@login_required
def orden_de_ensayo_list(request):
    """Muestra una lista de todas las órdenes de ensayo."""
    ordenes = OrdenDeEnsayo.objects.all().order_by('-fecha_entrega_programada')
    return render(request, 'orden_de_ensayo_list.html', {'ordenes': ordenes})

@login_required
def orden_de_ensayo_create(request):
    """Crea una nueva orden de ensayo."""
    if request.method == 'POST':
        form = OrdenDeEnsayoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('proyectos:orden_de_ensayo_list')
    else:
        form = OrdenDeEnsayoForm()
    return render(request, 'orden_de_ensayo_form.html', {'form': form, 'page_title': 'Crear Orden de Ensayo'})

@login_required
def orden_de_ensayo_update(request, pk):
    """Actualiza una orden de ensayo existente."""
    orden = get_object_or_404(OrdenDeEnsayo, pk=pk)
    if request.method == 'POST':
        form = OrdenDeEnsayoForm(request.POST, instance=orden)
        if form.is_valid():
            form.save()
            return redirect('proyectos:orden_de_ensayo_list')
    else:
        form = OrdenDeEnsayoForm(instance=orden)
    return render(request, 'orden_de_ensayo_form.html', {'form': form, 'page_title': 'Editar Orden de Ensayo'})

@login_required
def orden_de_ensayo_delete(request, pk):
    """Elimina una orden de ensayo."""
    orden = get_object_or_404(OrdenDeEnsayo, pk=pk)
    if request.method == 'POST':
        orden.delete()
        return redirect('proyectos:orden_de_ensayo_list')
    return render(request, 'orden_de_ensayo_confirm_delete.html', {'orden': orden})


# ----------------------------------------------------------------
# Vistas para Muestra
# ----------------------------------------------------------------
@login_required
def muestra_list(request):
    """Muestra una lista de todas las muestras."""
    muestras = Muestra.objects.all().order_by('-fecha_recepcion')
    return render(request, 'muestra_list.html', {'muestras': muestras})

@login_required
def muestra_create(request):
    """Crea una nueva muestra."""
    if request.method == 'POST':
        form = MuestraForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('proyectos:muestra_list')
    else:
        form = MuestraForm()
    return render(request, 'muestra_form.html', {'form': form, 'page_title': 'Crear Muestra'})

@login_required
def muestra_update(request, pk):
    """Actualiza una muestra existente."""
    muestra = get_object_or_404(Muestra, pk=pk)
    if request.method == 'POST':
        form = MuestraForm(request.POST, instance=muestra)
        if form.is_valid():
            form.save()
            return redirect('proyectos:muestra_list')
    else:
        form = MuestraForm(instance=muestra)
    return render(request, 'muestra_form.html', {'form': form, 'page_title': 'Editar Muestra'})

@login_required
def muestra_delete(request, pk):
    """Elimina una muestra."""
    muestra = get_object_or_404(Muestra, pk=pk)
    if request.method == 'POST':
        muestra.delete()
        return redirect('proyectos:muestra_list')
    return render(request, 'muestra_confirm_delete.html', {'muestra': muestra})


# ----------------------------------------------------------------
# Vistas para ResultadoEnsayo
# ----------------------------------------------------------------
@login_required
def resultado_ensayo_list(request):
    resultados = ResultadoEnsayo.objects.all()
    return render(request, 'resultado_ensayo_list.html', {'resultados': resultados, 'page_title': 'Lista de Resultados de Ensayo'})

@login_required
def resultado_ensayo_create(request):
    """Crea un nuevo resultado de ensayo."""
    if request.method == 'POST':
        form = ResultadoEnsayoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'El resultado de ensayo se ha creado con éxito.')
            return redirect('proyectos:resultado_ensayo_list')
        else:
            messages.error(request, 'Hubo un error al crear el resultado de ensayo. Por favor, revisa los datos.')
    else:
        form = ResultadoEnsayoForm()
    return render(request, 'resultado_ensayo_form.html', {'form': form, 'page_title': 'Crear Resultado de Ensayo'})

@login_required
def resultado_ensayo_update(request, pk):
    """Actualiza un resultado de ensayo existente."""
    resultado = get_object_or_404(ResultadoEnsayo, pk=pk)
    if request.method == 'POST':
        form = ResultadoEnsayoForm(request.POST, instance=resultado)
        if form.is_valid():
            form.save()
            messages.success(request, 'El resultado de ensayo se ha actualizado con éxito.')
            return redirect('proyectos:resultado_ensayo_list')
        else:
            messages.error(request, 'Hubo un error al actualizar el resultado de ensayo. Por favor, revisa los datos.')
    else:
        form = ResultadoEnsayoForm(instance=resultado)
    return render(request, 'resultado_ensayo_form.html', {'form': form, 'page_title': 'Editar Resultado de Ensayo'})

@login_required
def resultado_ensayo_delete(request, pk):
    resultado = get_object_or_404(ResultadoEnsayo, pk=pk)
    if request.method == 'POST':
        resultado.delete()
        messages.success(request, 'El resultado de ensayo se ha eliminado con éxito.')
        return redirect('proyectos:resultado_ensayo_list')
    return render(request, 'resultado_ensayo_confirm_delete.html', {'object': resultado, 'page_title': 'Eliminar Resultado de Ensayo'})


# ----------------------------------------------------------------
# Vistas para DocumentoFinal
# ----------------------------------------------------------------
login_required
def documento_final_list(request):
    """Muestra una lista de todos los documentos finales."""
    documentos = DocumentoFinal.objects.all().order_by('-fecha_emision')
    return render(request, 'documento_final_list.html', {'documentos': documentos})


@login_required
def documento_final_create(request):
    """Crea un nuevo documento final."""
    if request.method == 'POST':
        form = DocumentoFinalForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('proyectos:documento_final_list')
    else:
        form = DocumentoFinalForm()
    return render(request, 'documento_final_form.html', {'form': form, 'page_title': 'Crear Documento Final'})


@login_required
def documento_final_update(request, pk):
    """Actualiza un documento final existente."""
    documento = get_object_or_404(DocumentoFinal, pk=pk)
    if request.method == 'POST':
        form = DocumentoFinalForm(request.POST, request.FILES, instance=documento)
        if form.is_valid():
            form.save()
            return redirect('proyectos:documento_final_list')
    else:
        form = DocumentoFinalForm(instance=documento)
    return render(request, 'documento_final_form.html', {'form': form, 'page_title': 'Editar Documento Final'})


@login_required
def documento_final_delete(request, pk):
    """Elimina un documento final."""
    documento = get_object_or_404(DocumentoFinal, pk=pk)
    if request.method == 'POST':
        documento.delete()
        return redirect('proyectos:documento_final_list')
    return render(request, 'documento_final_confirm_delete.html', {'documento': documento})


# ================================================================
# Vistas para la generación de PDF
# ================================================================

def documento_final_pdf(request, pk):
    """
    Genera un informe en PDF de un Documento Final.
    """
    documento = get_object_or_404(DocumentoFinal, pk=pk)

    # Configuración del documento PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    # Estilos personalizados para el reporte
    styles.add(ParagraphStyle(name='TitleStyle', fontSize=24, leading=28, alignment=TA_CENTER, fontName='Helvetica-Bold'))
    styles.add(ParagraphStyle(name='HeadingStyle', fontSize=14, leading=18, fontName='Helvetica-Bold', spaceAfter=12))
    styles.add(ParagraphStyle(name='BodyStyle', fontSize=12, leading=16, alignment=TA_JUSTIFY, spaceAfter=8))
    styles.add(ParagraphStyle(name='SignatureStyle', fontSize=12, leading=16, spaceBefore=24, alignment=TA_CENTER))

    # Título del documento
    elements.append(Paragraph(documento.titulo, styles['TitleStyle']))
    elements.append(Spacer(1, 0.25 * inch))

    # Información del proyecto
    elements.append(Paragraph(f"<b>Proyecto:</b> {documento.proyecto.nombre_proyecto}", styles['BodyStyle']))
    elements.append(Paragraph(f"<b>Cliente:</b> {documento.proyecto.cliente.razon_social}", styles['BodyStyle']))
    elements.append(Paragraph(f"<b>Fecha de Emisión:</b> {documento.fecha_emision}", styles['BodyStyle']))
    elements.append(Spacer(1, 0.25 * inch))

    # Resumen Ejecutivo
    elements.append(Paragraph("Resumen Ejecutivo", styles['HeadingStyle']))
    if documento.resumen_ejecutivo_ia:
        elements.append(Paragraph(documento.resumen_ejecutivo_ia, styles['BodyStyle']))
    else:
        elements.append(Paragraph("No se proporcionó un resumen ejecutivo.", styles['BodyStyle']))
    elements.append(Spacer(1, 0.25 * inch))

    # Análisis Detallado
    elements.append(Paragraph("Análisis Detallado", styles['HeadingStyle']))
    if documento.analisis_detallado_ia:
        elements.append(Paragraph(documento.analisis_detallado_ia, styles['BodyStyle']))
    else:
        elements.append(Paragraph("No se proporcionó un análisis detallado.", styles['BodyStyle']))
    elements.append(Spacer(1, 0.25 * inch))

    # Resultados de Ensayos
    elements.append(Paragraph("Resultados de Ensayos", styles['HeadingStyle']))
    resultados = ResultadoEnsayo.objects.filter(muestra__orden__proyecto=documento.proyecto)
    if resultados.exists():
        for res in resultados:
            elements.append(Paragraph(f"<b>Muestra:</b> {res.muestra.codigo_muestra}", styles['BodyStyle']))
            if res.resultados_json:
                elements.append(Paragraph(f"<b>Resultados:</b> {res.resultados_json}", styles['BodyStyle']))
            if res.observaciones:
                elements.append(Paragraph(f"<b>Observaciones:</b> {res.observaciones}", styles['BodyStyle']))
            elements.append(Spacer(1, 0.1 * inch))
    else:
        elements.append(Paragraph("No hay resultados de ensayos asociados a este proyecto.", styles['BodyStyle']))
    elements.append(Spacer(1, 0.25 * inch))

    # Recomendaciones
    elements.append(Paragraph("Recomendaciones", styles['HeadingStyle']))
    if documento.recomendaciones_ia:
        elements.append(Paragraph(documento.recomendaciones_ia, styles['BodyStyle']))
    else:
        elements.append(Paragraph("No se proporcionaron recomendaciones.", styles['BodyStyle']))
    elements.append(Spacer(1, 0.25 * inch))

    # Firmas
    elements.append(Paragraph("--- Firmas ---", styles['SignatureStyle']))
    if documento.firma_supervisor:
        firma_path = os.path.join(settings.MEDIA_ROOT, documento.firma_supervisor.name)
        if os.path.exists(firma_path):
            img = ReportLabImage(firma_path, width=1.5*inch, height=0.75*inch)
            elements.append(img)
            elements.append(Paragraph("Firma del Supervisor", styles['SignatureStyle']))
            
    if documento.firma_cliente:
        firma_path = os.path.join(settings.MEDIA_ROOT, documento.firma_cliente.name)
        if os.path.exists(firma_path):
            img = ReportLabImage(firma_path, width=1.5*inch, height=0.75*inch)
            elements.append(img)
            elements.append(Paragraph("Firma del Cliente", styles['SignatureStyle']))
    
    # Construir el documento
    doc.build(elements)

    # Preparar la respuesta HTTP
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="informe_{documento.proyecto.nombre_proyecto}.pdf"'
    response.write(buffer.getvalue())
    buffer.close()
    return response

# ================================================================
# Vistas de la aplicación Proyectos
# (manteniendo el resto de tus vistas existentes si las tuvieras)
# ================================================================
def proyecto_list(request):
    proyectos = Proyecto.objects.all()
    return render(request, 'proyecto_list.html', {'proyectos': proyectos})
