from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'index.html')


@login_required
def dashboard_view(request):
    """
    Vista del dashboard que solo es accesible para usuarios autenticados.
    """
    return render(request, 'dashboard.html')

