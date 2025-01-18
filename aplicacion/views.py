from django.shortcuts import render
from django.views.generic import ListView ,TemplateView, CreateView, DetailView, UpdateView
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
from django.urls import reverse_lazy
from django.contrib.auth.forms import *


# Create your views here.
class HomeView(TemplateView):
    template_name = 'home.html'

class RegistroParticularView(CreateView):
    form_class = UsuarioParticularCreationForm
    template_name = 'registration/registro_particular.html'
    success_url = reverse_lazy('login')

class RegistroEmpresaView(CreateView):
    form_class = UsuarioEmpresaCreationForm
    template_name = 'registration/registro_empresa.html'
    success_url = reverse_lazy('login')

class PrincipalView(LoginRequiredMixin, TemplateView):
    model = Usuario
    template_name = 'principal.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nombre'] = self.request.user.username
        return context

class UsuarioActualizarPerfil(LoginRequiredMixin, UpdateView):
    model = Usuario
    template_name = 'perfil.html'
    fields = ['username', 'email', 'biografia', 'foto_perfil', 'rol', 'instagram', 'tiktok', 'otras_rrss']


    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario'] = self.request.user
        return context
    
    def get_success_url(self):
        return reverse_lazy('principal')



    


    


    """
    def get_context_data(self, **kwargs):
    
    Es un METODO que puedes sobrescribir en las vistas basadas en clases para PERSONALIZAR 
    los DATOS ENVIADOS al CONTEXTO. self es la instancia de la clase (PrincipalView).
    **kwargs permite capturar cualquier argumento adicional que se pase al contexto(parámetros desde la URL).

    context = super().get_context_data(**kwargs)


    Llama al método get_context_data de la clase base de la vista (la que estás heredando).
    Este método devuelve un diccionario (context) con los datos que la clase base ya estaba 
    agregando al contexto.
    **kwargs se pasa al método base para asegurarte de que todos los datos esperados se procesen 
    correctamente.

    context['nombre'] = self.request.user.username

    Aquí se agrega una nueva clave 'nombre' al diccionario context
    
    """