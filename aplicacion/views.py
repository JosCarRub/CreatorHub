from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.views.generic import ListView ,TemplateView, CreateView, DetailView, UpdateView, DeleteView
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
from django.urls import reverse_lazy
from django.contrib.auth.forms import *
from django.contrib import messages


# Create your views here.
class HomeView(TemplateView):
    template_name = 'home.html'


#REGISTRO
class RegistroParticularView(CreateView):
    form_class = UsuarioParticularCreationForm
    template_name = 'registration/registro_particular.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        messages.success(self.request,'Usuario creado correctamente')
        return super().form_valid(form)

class RegistroEmpresaView(CreateView):
    form_class = UsuarioEmpresaCreationForm
    template_name = 'registration/registro_empresa.html'
    success_url = reverse_lazy('login')




class PrincipalView(LoginRequiredMixin, TemplateView):
    model = Usuario
    template_name = 'principal.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario'] = self.request.user
        return context


#CRUD PERFIL    
class UsuarioPerfilView(LoginRequiredMixin, TemplateView):
    model = Usuario
    template_name = 'perfil/perfil.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario'] = self.request.user
        return context
    

class UsuarioActualizarPerfilView(LoginRequiredMixin, UpdateView):
    model = Usuario
    template_name = 'perfil/perfil_actualizar.html'
    fields = ['username', 'email', 'biografia', 'foto_perfil', 'rol', 'instagram', 'tiktok', 'otras_rrss']


    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario'] = self.request.user
        return context
    
    def get_success_url(self):
        return reverse_lazy('perfil')

class UsuarioBorrarPerfilView(LoginRequiredMixin, DeleteView):
    model = Usuario
    template_name = 'perfil/perfil_borrar.html'
    success_url = reverse_lazy('principal')

    def get_object(self, queryset=None):         # Retorna el usuario actual (self.request.user)
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario'] = self.request.user
        return context
    
#OFERTAS
class CrearOfertaView(LoginRequiredMixin, CreateView):
    model = Oferta
    form_class = CrearOfertaForm
    template_name = 'oferta/crear_oferta.html'
    success_url = reverse_lazy('perfil')

      #VALIDACION
    def form_valid(self, form):
        oferta = form.save(commit=False)
        oferta.usuario = self.request.user # Si no no se rellena el campo ID
        oferta.save()
        return super().form_valid(form)
    


class ListadoOfertasView(LoginRequiredMixin, ListView):
    model = Oferta
    template_name = 'oferta/lista_ofertas.html'
    context_object_name = 'ofertas'

    def get_queryset(self):
        return Oferta.objects.all().order_by('-fecha_publicacion')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_ofertas'] = Oferta.objects.count()
        return context

#BORRAR Y ACTUALIZAR OFERTAS


#APLICAR A OFERTAS

    


    


    """
    def get_context_data(self, **kwargs):
    
    Es un METODO con el que puedo sobrescribir las vistas basadas en clases para PERSONALIZAR 
    los DATOS ENVIADOS al CONTEXTO. 
    self es la instancia de la clase (PrincipalView).

    **kwargs permite capturar cualquier argumento adicional que se pase al contexto(parámetros desde la URL).

    context = super().get_context_data(**kwargs)


    Llama al método get_context_data de la clase base de la vista (la que estoy heredando).
    Este método devuelve un diccionario (context) con los datos que la clase base ya estaba 
    agregando al contexto.
    
    **kwargs se pasa al método base para asegurarte de que todos los datos esperados se procesen 
    correctamente.

    context['nombre'] = self.request.user.username

    Aquí se agrega una nueva clave 'nombre' al diccionario context
    
    """