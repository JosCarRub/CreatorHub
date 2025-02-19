from datetime import date
from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


#REGISTRO USUARIOS
class UsuarioParticularCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'biografia', 'foto_perfil', 'rol') #SÉ que se pueden quitar bio y foto 
        widgets = {
            'biografia': forms.Textarea(attrs={'maxlength': 420}),  # Agregar el límite en el HTML
        }
    
    def clean_username(self):
        username = self.cleaned_data.get('username')

        if Usuario.objects.filter(username=username).exists():
            raise ValidationError('Este nombre de usuario ya está registrado, ¡debes elegir otro!')

        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')  

        if email and Usuario.objects.filter(email=email).exists():
            raise ValidationError('El email introducido ya está registrado, ¡debes introducir otro!')

        return email 
    
     
    
class UsuarioEmpresaCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'biografia', 'foto_perfil', 'rol')
        widgets = {
            'biografia': forms.Textarea(attrs={'maxlength': 420}), 
        }
    
    def clean_username(self):
        username = self.cleaned_data.get('username')

        if Usuario.objects.filter(username=username).exists():
            raise ValidationError('Este nombre de usuario ya está registrado, ¡debes elegir otro!')

        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')  

        if email and Usuario.objects.filter(email=email).exists():
            raise ValidationError('El email introducido ya está registrado, ¡debes introducir otro!')
        return email  

class UsuarioRedesCreationForm(forms.ModelForm):
    class Meta:
        model = RedesSocialesUsuario
        fields = ('instagram', 'tiktok', 'youtube', 'twicht')


#CRUD OFERTAS
class CrearOfertaForm(forms.ModelForm):
    class Meta:
        model = Oferta
        fields = ('descripcion', 'requisitos', 'tiktok', 'instagram', 'youtube','twitch', 'fecha_expiracion') 
        widgets = {

                'fecha_expiracion': forms.DateInput(format='%Y-%m-%d',attrs={'type': 'date'}),
            }
        
        help_texts = {
            'tiktok': 'Selecciona esta casilla si tu oferta está relacionada con TikTok.',
            'instagram': 'Selecciona esta casilla si tu oferta está relacionada con Instagram.',
            'youtube': 'Selecciona esta casilla si tu oferta está relacionada con YouTube.',
            'twitch': 'Selecciona esta casilla si tu oferta está relacionada con Twitch.',
        }

        def clean_fecha_expiracion(self):
            fecha_expiracion = self.cleaned_data.get('fecha_expiracion')
            if fecha_expiracion < date.today():
                raise forms.ValidationError('La fecha de expiración no puede ser anterior a hoy.')
            return fecha_expiracion

class AplicacionOfertaForm(forms.ModelForm):
    class Meta:
        model = AplicacionOferta
        fields = []

class PuntuarAplicacionForm(forms.ModelForm):
    class Meta:
        model = AplicacionOferta
        fields = ['puntuacion']



       

        



