# trabajadores/views.py 
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import TrabajadorProfile
from .forms import TrabajadorProfileForm

## Vistas para el CRUD
def trabajadores_view(request):
    return render(request, 'trabajadores/trabajadores-principal.html')
# Read (Listar todos los perfiles)
class TrabajadorListView(LoginRequiredMixin, ListView):
    model = TrabajadorProfile
    template_name = 'trabajadores/trabajador_list.html'
    context_object_name = 'trabajadores'

# Read (Ver un perfil en detalle)
class TrabajadorDetailView(LoginRequiredMixin, DetailView):
    model = TrabajadorProfile
    template_name = 'trabajadores/trabajador_detail.html'
    context_object_name = 'trabajador'

# Create (Crear un nuevo perfil)
class TrabajadorCreateView(LoginRequiredMixin, CreateView):
    model = TrabajadorProfile
    form_class = TrabajadorProfileForm
    template_name = 'trabajadores/trabajador_form.html'
    success_url = reverse_lazy('trabajador_list')

# Update (Actualizar un perfil existente)
class TrabajadorUpdateView(LoginRequiredMixin, UpdateView):
    model = TrabajadorProfile
    form_class = TrabajadorProfileForm
    template_name = 'trabajadores/trabajador_form.html'
    success_url = reverse_lazy('trabajador_list')

# Delete (Eliminar un perfil)
class TrabajadorDeleteView(LoginRequiredMixin, DeleteView):
    model = TrabajadorProfile
    template_name = 'trabajadores/trabajador_confirm_delete.html'
    success_url = reverse_lazy('trabajador_list')