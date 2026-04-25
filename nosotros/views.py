from django.shortcuts import render
from nosotros.models import DocumentoNosotros


def nosotros_view(request):
    documentos = DocumentoNosotros.objects.filter(
        activo=True
    ).select_related('tipo').order_by(
        'orden',
        '-destacado',
        '-creado'
    )

    context = {
        'documentos': documentos,
        'documentos_principales': documentos[:4],
        'documentos_restantes': documentos[4:],
    }

    return render(request, 'inicio/index.html', context)