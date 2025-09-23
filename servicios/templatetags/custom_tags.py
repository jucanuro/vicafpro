from django import template
import os

register = template.Library()

@register.filter
def basename(value):
    """
    Retorna el nombre base de una ruta de archivo.
    Ejemplo: 'media/images/photo.jpg' -> 'photo.jpg'
    """
    if not value:
        return ''
    return os.path.basename(value)