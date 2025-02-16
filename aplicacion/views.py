from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView ,TemplateView, CreateView, DetailView, UpdateView, DeleteView, FormView
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
from django.urls import reverse_lazy
from django.contrib.auth.forms import *
from django.contrib import messages
from django.forms import inlineformset_factory, modelformset_factory
from django.core.mail import send_mail



# Create your views here.
class HomeView(TemplateView):
    template_name = 'principales/home.html'


#REGISTRO
class RegistroParticularView(CreateView):
    form_class = UsuarioParticularCreationForm
    template_name = 'registration/registro_particular.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
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
   
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["ofertas_empresa"] = Oferta.objects.filter(
            usuario=self.request.user
            ).order_by('-fecha_publicacion')
        
        context['ofertas_tipos'] = TipoDeOferta.objects.filter(
            oferta__usuario=self.request.user)
        
        aplicaciones_por_oferta = {
            oferta.pk: AplicacionOferta.objects.filter(oferta=oferta).count()
            for oferta in context["ofertas"]
        }

        context["ofertas_aplicaciones"] = aplicaciones_por_oferta
        
        return context
    

    
    


#CRUD PERFIL    
class UsuarioPerfilView(LoginRequiredMixin, TemplateView):
    model = Usuario
    template_name = 'perfil/perfil.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario'] = self.request.user

        context['redes_usuario'] = RedesSocialesUsuario.objects.filter(
            usuario = self.request.user
        ).first()


        numero_ofertas_publicadas = Oferta.objects.filter(
            usuario=self.request.user
            ).count()
        
        context['numero_ofertas_publicadas'] = numero_ofertas_publicadas


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

#ACTUALIZAR REDES EN PERFIL USUARIO
class UsuarioActualizarRedesView(LoginRequiredMixin, UpdateView):
    model = RedesSocialesUsuario
    fields = ['instagram', 'tiktok', 'youtube', 'twicht']
    template_name = 'perfil/perfil_actualizar_redes.html'
    success_url = reverse_lazy('perfil')

    

class UsuarioBorrarPerfilView(LoginRequiredMixin, DeleteView):
    model = Usuario
    template_name = 'perfil/perfil_borrar.html'
    success_url = reverse_lazy('principal')

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario'] = self.request.user
        return context

class UsuarioCompletarRedesView(LoginRequiredMixin, CreateView):
    form_class = UsuarioRedesCreationForm
    template_name = 'perfil/perfil_completar_redes.html'
    success_url = reverse_lazy('perfil')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.usuario = self.request.user  # asignar el usuario a la oferta, si no no se rellena el campo ID de usuario
        self.object.save()
        return super().form_valid(form)
    


        





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

        if self.request.POST:
            context['tipoOferta_formset'] = TiposDeOfertaFormSet(self.request.POST)

        else:
            context['tipoOferta_formset'] = TiposDeOfertaFormSet()
        return context
    
    
    
    def form_valid(self, form):
        context = self.get_context_data()
        tipoOferta_formset = context['tipoOferta_formset']

        self.object = form.save(commit=False)
        self.object.usuario = self.request.user  # asignar el usuario a la oferta, si no no se rellena el campo ID de usuario
        self.object.save()


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
            return self.form_invalid(form)  

    

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



class DetalleOfertaView(LoginRequiredMixin, DetailView):
    model = Oferta
    template_name = 'oferta/detalle_oferta.html'


class AplicarOfertaView(LoginRequiredMixin, CreateView):
    model = AplicacionOferta
    fields = []
    success_url = reverse_lazy('perfil')

    def form_valid(self,form):
        oferta = get_object_or_404(Oferta, pk=self.kwargs['pk'])
        self.object = form.save(commit=False)
        self.object.usuario = self.request.user
        self.object.oferta = oferta
        self.object.fecha_expiracion = oferta.fecha_expiracion
        
        self.object.save()

        return super().form_valid(form)

class DetalleAspirantesOfertaView(LoginRequiredMixin, DetailView):
    model = Oferta
    template_name = 'oferta/aplicaciones/detalle_aspirantes_oferta.html'
    context_object_name = 'oferta'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        aplicaciones = AplicacionOferta.objects.filter(oferta=self.object)
        
        # diccionario en el que guardaremos las redes sociales los usuarios
        redes_por_usuario = {}

        for aplicacion in aplicaciones:
            usuario = aplicacion.usuario
            # redes sociales de cada usuario
            redes = RedesSocialesUsuario.objects.filter(usuario=usuario).first()
            redes_por_usuario[usuario.id] = redes  # Guardamos las redes de cada usuario en el diccionario
        
        context['aplicaciones'] = aplicaciones
        context['redes_por_usuario'] = redes_por_usuario  
        return context
    
    def post(self, request, *args, **kwargs):
        
        oferta = self.get_object()
        
        aplicacion_id = request.POST.get('aplicacion_id')
        aplicacion = AplicacionOferta.objects.get(id=aplicacion_id)

        estado = request.POST.get('estado')
        boolean_oferta = True

        if estado == 'aceptada' and aplicacion.estado_aplicacion != 'aceptada': #que haya cambio para que no haya envío de correos en un get
            aplicacion.estado_aplicacion = 'aceptada'
            aplicacion.save()
            self.enviar_correo(aplicacion.usuario.id, boolean_oferta)

        elif estado == 'denegada':
            aplicacion.estado_aplicacion = 'denegada'
            aplicacion.save()
            boolean_oferta = False
            self.enviar_correo(aplicacion.usuario.id, boolean_oferta)
        
        

        
        return redirect('detalle_aspirantes_oferta', pk=oferta.pk)

    def correo_aceptada(self, email_destino):
        subject = "¡Tu oferta ha sido aceptada!"
        message = "¡Felicidades! Tu aplicación ha sido aceptada. Puedes continuar con el siguiente paso."
        from_email = 'ddjangoappservidor@gmail.com'
        email_usuario = email_destino
        send_mail(subject, message, from_email, [email_usuario])
    
    def correo_denegada(self, email_destino):
        subject = "¡Desafortunadamente tu aplicación a ha sido denegada!"
        message = "¡Lo sentimos! Tu aplicación ha sido denegada."
        from_email = 'ddjangoappservidor@gmail.com'
        email_usuario = email_destino
        send_mail(subject, message, from_email, [email_usuario])

    def enviar_correo(self, usuario_id, boolean_oferta):
        try:
            usuario = Usuario.objects.get(id=usuario_id) 
            email_destino = usuario.email
            if boolean_oferta:
                self.correo_aceptada(email_destino)  
                print(f"Correo enviado a {email_destino}")
            else:
                self.correo_denegada(email_destino)  
                print(f"Correo enviado a {email_destino}")


        except Usuario.DoesNotExist:
            print("Error: Usuario no encontrado")






    

    

    
    






  
#CANCELAR = CAMBIAR ESTADO --> OFERTAS


#APLICAR A OFERTAS

















    







    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     ofertas = Oferta.objects.all().distinct()
    #     context["ofertas"] = ofertas

    #     #Línea para crear campos de otro modelo en un formulario de un modelo padre
    #     TiposDeOfertaFormSet = inlineformset_factory(Oferta, TipoDeOferta, fields=['tipo'], extra=1, can_delete=False)
    #     RedesSocialesOfertaFormSet = inlineformset_factory(Oferta, RedesSocialesOferta, fields=['instagram', 'tiktok', 'youtube'], extra=1, can_delete=False)

    #     if self.request.POST:
    #         context['tipoOferta_formset'] = TiposDeOfertaFormSet(self.request.POST)
    #         context['redesSociales_formset'] = RedesSocialesOfertaFormSet(self.request.POST)

    #     else:
    #         context['tipoOferta_formset'] = TiposDeOfertaFormSet()
    #         context['redesSociales_formset'] = RedesSocialesOfertaFormSet()
    #     return context
    
    
    
    # def form_valid(self, form):
    #     context = self.get_context_data()
    #     tipoOferta_formset = context['tipoOferta_formset']
    #     redesSociales_formset = context['redesSociales_formset']

    #     self.object = form.save(commit=False)
    #     self.object.usuario = self.request.user  # asignar el usuario a la oferta, si no no se rellena el campo ID de usuario
    #     self.object.save()

    #     if redesSociales_formset.is_valid():
    #         rrss = redesSociales_formset.save(commit=False)

    #         rrss.oferta = self.object
    #         rrss.usuario = self.request.user
    #         rrss.save()
    #     else:
    #         return self.form_invalid(form)

    #     if tipoOferta_formset.is_valid():  
    #         tipos = tipoOferta_formset.save(commit=False) 

    #         if not tipos: 
    #             form.add_error(None, "Debes seleccionar al menos un tipo de oferta. Si no encuentras ninguna categoría adecuada, selecciona 'Otra'.\n ¡Si quieres proponer una nueva categoría que no exista, ponte en contacto con nosotros!")
    #             return self.form_invalid(form)

    #         for tipo in tipos:
    #             tipo.oferta = self.object  # Relacionamos cada tipo con la oferta creada
    #             tipo.save()  # Guardamos en la BD cada TipoDeOferta
    #         return super().form_valid(form)  # Si todo es válido, continuar con la vista
    #     else:
    #         return self.form_invalid(form)  # Si el formset no es válido, rechazar la solicitud


    


  
