from django.shortcuts import render

def trabajadores_view(request):
    return render(request, 'trabajadores/trabajadores.html')
