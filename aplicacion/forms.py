from datetime import date
from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


#REGISTRO USUARIOS
class UsuarioParticularCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'biografia', 'foto_perfil', 'rol')
        widgets = {
            'biografia': forms.Textarea(attrs={'maxlength': 420}),  # Agregar el límite en el HTML
        }
    
class UsuarioEmpresaCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'biografia', 'foto_perfil', 'rol')
        widgets = {
            'biografia': forms.Textarea(attrs={'maxlength': 420}), 
        }

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

class AplicacionOfertaForm(forms.ModelForm):
    class Meta:
        model = AplicacionOferta
        fields = []



       

        



