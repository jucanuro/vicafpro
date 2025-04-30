from django.shortcuts import render

def servicios_view(request):
    return render(request, 'servicios/servicios.html')
