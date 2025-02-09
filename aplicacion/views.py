from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView ,TemplateView, CreateView, DetailView, UpdateView, DeleteView
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
from django.urls import reverse_lazy
from django.contrib.auth.forms import *
from django.contrib import messages
from django.forms import inlineformset_factory



# Create your views here.
class HomeView(TemplateView):
    template_name = 'principales/home.html'


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



#PRINCIPAL
class PrincipalListadoOfertasView(LoginRequiredMixin, ListView):
    model = Oferta
    template_name = 'principales/principal.html'
    context_object_name = 'ofertas'

    def get_queryset(self):
        return Oferta.objects.all().order_by('-fecha_publicacion')

    def get_context_data_ofertas(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_ofertas'] = Oferta.objects.count()
        # context['ofertas'] = Oferta.objects.distinct()
        return context
    
    def get_queryset(self):

        query = super().get_queryset()
        filtro_tipo = self.request.GET.get("filtro_tipo")
        filtro_plataformas = self.request.GET.get("filtro_plataformas")

        if filtro_tipo :
            query = query.filter(tipo__icontains = filtro_tipo)
        
        if filtro_plataformas:
            query = query.filter(plataformas__nombre = filtro_plataformas)
        
        return query

    
    


#CRUD PERFIL    
class UsuarioPerfilView(LoginRequiredMixin, TemplateView):
    model = Usuario
    template_name = 'perfil/perfil.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario'] = self.request.user
        # context['ofertas'] = usuario.ofertas.all().order_by('-fecha_publicacion')

        return context
    

class UsuarioActualizarPerfilView(LoginRequiredMixin, UpdateView):
    model = Usuario
    template_name = 'perfil/perfil_actualizar.html'
    fields = ['username', 'email', 'biografia', 'foto_perfil', 'rol']


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ofertas = Oferta.objects.all().distinct()
        context["ofertas"] = ofertas

        #Línea para crear campos de otro modelo en un formulario de un modelo padre
        TiposDeOfertaFormSet = inlineformset_factory(Oferta, TipoDeOferta, fields=['tipo'], extra=1, can_delete=False)
        RedesSocialesOfertaFormSet = inlineformset_factory(Oferta, RedesSocialesOferta, fields=['instagram', 'tiktok', 'youtube'], extra=1, can_delete=False)

        if self.request.POST:
            context['tipoOferta_formset'] = TiposDeOfertaFormSet(self.request.POST)
            context['redesSociales_formset'] = RedesSocialesOfertaFormSet(self.request.POST)

        else:
            context['tipoOferta_formset'] = TiposDeOfertaFormSet()
            context['redesSociales_formset'] = RedesSocialesOfertaFormSet()
        return context
    
    
    
    def form_valid(self, form):
        context = self.get_context_data()
        tipoOferta_formset = context['tipoOferta_formset']
        redesSociales_formset = context['redesSociales_formset']

        self.object = form.save(commit=False)
        self.object.usuario = self.request.user  # asignar el usuario a la oferta, si no no se rellena el campo ID de usuario
        self.object.save()

        if redesSociales_formset.is_valid():
            rrss = redesSociales_formset.save(commit=False)

            rrss.oferta = self.object
            rrss.usuario = self.request.user
            rrss.save()
        else:
            return self.form_invalid(form)

        if tipoOferta_formset.is_valid():  
            tipos = tipoOferta_formset.save(commit=False) 

            if not tipos: 
                form.add_error(None, "Debes seleccionar al menos un tipo de oferta. Si no encuentras ninguna categoría adecuada, selecciona 'Otra'.\n ¡Si quieres proponer una nueva categoría que no exista, ponte en contacto con nosotros!")
                return self.form_invalid(form)

            for tipo in tipos:
                tipo.oferta = self.object  # Relacionamos cada tipo con la oferta creada
                tipo.save()  # Guardamos en la BD cada TipoDeOferta
            return super().form_valid(form)  # Si todo es válido, continuar con la vista
        else:
            return self.form_invalid(form)  # Si el formset no es válido, rechazar la solicitud
    
    


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



class ActualizarOfertaView(LoginRequiredMixin, UpdateView):
    model = Oferta
    template_name = 'oferta/actualizar_oferta.html'
    form_class = CrearOfertaForm
    fields = '__all__'
    success_url = reverse_lazy('lista_ofertas')

  
#BORRAR OFERTAS

#APLICAR A OFERTAS

    


    


  
