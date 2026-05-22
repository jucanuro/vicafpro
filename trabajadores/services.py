from .models import Trabajador


def obtener_trabajadores():
    return {
        'trabajadores': Trabajador.objects.all()
    }