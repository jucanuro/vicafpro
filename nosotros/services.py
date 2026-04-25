from .models import DocumentoNosotros


def obtener_documentos_nosotros():
    documentos = list(
        DocumentoNosotros.objects.filter(activo=True)
        .select_related('tipo')
        .order_by('orden', '-destacado', '-creado')
    )

    return {
        'documentos': documentos,
        'documentos_principales': documentos[:4],
        'documentos_restantes': documentos[4:],
    }