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
from django.db.models import Count



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
    paginate_by= 5
   
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

        total_ofertas = self.get_queryset().count()

        context['total'] = total_ofertas

        context["ofertas_aplicaciones"] = aplicaciones_por_oferta
        
        return context
    

    def get_queryset(self):
        query = super().get_queryset()

        plataforma = self.request.GET.get("plataforma")
        tipo_oferta = self.request.GET.get("tipo_oferta")


        if plataforma == "instagram":
            query = query.filter(instagram=True)
        elif plataforma == "tiktok":
            query = query.filter(tiktok=True)
        elif plataforma == "youtube":
            query = query.filter(youtube=True)
        elif plataforma == "twitch":
            query = query.filter(twitch=True)

        if tipo_oferta:
            query = query.filter(get_oferta_tipos__tipo=tipo_oferta)


        

        return query


class TopUsuariosView(LoginRequiredMixin, ListView):
    model = Usuario
    template_name = 'principales/top_usuarios.html'

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        top_usuarios = Usuario.objects.filter(rol='PARTICULAR'
        ).annotate(trabajos_realizados=Count('num_trabajos')
        ).order_by('-puntuacion_promedio', '-num_trabajos')[:10] 
        
        context['top_usuarios'] = top_usuarios

        if top_usuarios.count() > 10:
            top_usuarios = top_usuarios[:10]
        
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
        messages.success(self.request, 'Perfil actualizado con éxito')
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
        messages.success(self.request, '¡Enhorabuena! Redes sociales completadas')
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
                messages.error(self.request, "Debes seleccionar al menos un tipo de oferta. Si no encuentras ninguna categoría adecuada, selecciona 'Otra'.\n ¡Si quieres proponer una nueva categoría que no exista, ponte en contacto con nosotros!")
                return self.form_invalid(form)

            for tipo in tipos:
                tipo.oferta = self.object  # Relacionamos cada tipo con la oferta creada
                tipo.save()  # Guardamos en la BD cada TipoDeOferta

            messages.success(self.request, "¡Oferta creada exitosamente!")
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
        usuario = self.request.user

        if AplicacionOferta.objects.filter(usuario=usuario, oferta=oferta).exists():
            self.form_invalid(form)
            messages.error(self.request, "Ya has aplicado a esta oferta")
            return redirect('detalle_oferta', pk=self.kwargs['pk'])


        self.object = form.save(commit=False)
        self.object.usuario = usuario
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
        aplicacion = get_object_or_404(AplicacionOferta, id=aplicacion_id)

        estado = request.POST.get('estado')
        boolean_oferta = True

        if estado == 'aceptada' and aplicacion.estado_aplicacion != 'aceptada': #que haya cambio para que no haya envío de correos en un get
            aplicacion.estado_aplicacion = 'aceptada'
            aplicacion.save()
            self.enviar_correo(aplicacion.usuario.id, boolean_oferta)
            messages.success(self.request, "¡Email enviado al usuario!")

        elif estado == 'denegada' and aplicacion.estado_aplicacion != 'denegada':
            aplicacion.estado_aplicacion = 'denegada'
            aplicacion.save()
            boolean_oferta = False
            self.enviar_correo(aplicacion.usuario.id, boolean_oferta)
            messages.success(self.request, "¡Email enviado al usuario!")
        
        return redirect('detalle_aspirantes_oferta', pk=oferta.pk)
    

    def correo_aceptada(self, email_destino):
        subject = "¡Tu oferta ha sido aceptada!"
        message = "¡Felicidades! Tu aplicación ha sido aceptada."
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
            if not usuario.email:
                print(f"Error: Usuario {usuario_id} no tiene email registrado.")
                
            
            if boolean_oferta:
                self.correo_aceptada(email_destino)  
                print(f"Correo enviado a {email_destino}")
            else:
                self.correo_denegada(email_destino)  
                print(f"Correo enviado a {email_destino}")


        except Usuario.DoesNotExist:
            print("Error: Usuario no encontrado")
    
class PuntuarAplicacionView(LoginRequiredMixin, UpdateView):
        model = AplicacionOferta
        form_class = PuntuarAplicacionForm
        template_name = 'oferta/aplicaciones/puntuar_aspirante_oferta.html'
        success_url = reverse_lazy('principal')

        def get_object(self, queryset=None):
            #coger oferta y la aplicación desde la url
            oferta = get_object_or_404(Oferta, pk=self.kwargs['oferta_id'])
            aplicacion = get_object_or_404(AplicacionOferta, oferta=oferta, pk=self.kwargs['aplicacion_id'])
            return aplicacion  # retorno la aplicación relacionada con la oferta


        
        
        def form_valid(self, form):

            aplicacion = form.instance
            

            if aplicacion.trabajo_puntuado:
                
                messages.error(self.request, "¡No puedes puntuar un trabajo más de una vez!")
                return self.form_invalid(form)
            
            usuario = aplicacion.usuario

            form.instance.puntuacion = form.cleaned_data['puntuacion']
            aplicacion.puntuacion = form.instance.puntuacion
            aplicacion.trabajo_puntuado = True 
            form.instance.save()

            #sumamos el trabajo realizado al modelo usuario
            usuario.num_trabajos += 1
            usuario.save()

            #calcular aplicaciones aceptadas del usuario
            aplicaciones = AplicacionOferta.objects.filter(usuario=usuario, estado_aplicacion='aceptada')


            total_puntuacion = sum([int(app.puntuacion) for app in aplicaciones if app.puntuacion])  # sumar las puntuaciones

            if usuario.num_trabajos > 0:
                nuevo_promedio = total_puntuacion / usuario.num_trabajos

            
            usuario.puntuacion_promedio = nuevo_promedio
            usuario.save()

            messages.success(self.request, "¡Puntuación registrada!")

            return redirect('detalle_aspirantes_oferta', pk=form.instance.oferta.pk)


    


  
