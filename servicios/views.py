from django.shortcuts import render

def servicios_view(request):
    return render(request, 'servicios/servicios.html')

def detalleservicios_view(request):
    return render(request, 'servicios/detalleservicios.html')