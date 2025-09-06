from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import ClienteProfile
from .forms import ClienteProfileForm


class ClienteListView(ListView):
    """
    Vista para mostrar una lista de todos los clientes.
    """
    model = ClienteProfile
    template_name = 'clientes/clientes_list.html'
    context_object_name = 'object_list' 

class ClienteCreateView(LoginRequiredMixin, CreateView):
    model = ClienteProfile
    form_class = ClienteProfileForm
    template_name = 'clientes/clientes_form.html'
    success_url = reverse_lazy('lista_clientes')

    def dispatch(self, request, *args, **kwargs):
        # Si el usuario ya tiene un perfil, redirigirlo a la lista de clientes
        if ClienteProfile.objects.filter(user=request.user).exists():
            return redirect('lista_clientes') 
            
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ClienteUpdateView(LoginRequiredMixin, UpdateView):
    """
    Vista para editar un perfil de cliente existente.
    """
    model = ClienteProfile
    form_class = ClienteProfileForm
    template_name = 'clientes/clientes_form.html'
    success_url = reverse_lazy('lista_clientes')

class ClienteDeleteView(LoginRequiredMixin, DeleteView):
    """
    Vista para eliminar un perfil de cliente.
    """
    model = ClienteProfile
    template_name = 'clientes/clientes_confirm_delete.html'
    success_url = reverse_lazy('lista_clientes')
