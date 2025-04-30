from django.shortcuts import render

def clientes_view(request):
    return render(request, 'clientes/clientes.html')
