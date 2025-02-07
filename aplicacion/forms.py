from datetime import date
from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


#REGISTRO USUARIOS
class UsuarioParticularCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'biografia', 'foto_perfil', 'rol', 'instagram', 'tiktok', 'otras_rrss')
        widgets = {
            'biografia': forms.Textarea(attrs={'maxlength': 420}),  # Agregar el límite en el HTML
        }
    
class UsuarioEmpresaCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'biografia', 'foto_perfil', 'rol')
        widgets = {
            'biografia': forms.Textarea(attrs={'maxlength': 420}),  # Agregar el límite en el HTML
        }

#PERFIL USUARIO
# class UsuarioActualizarPerfilForm(forms.ModelForm):
#     class Meta:
#         model = get_user_model()
#         fields = ('username', 'email', 'biografia', 'foto_perfil', 'rol', 'instagram', 'tiktok', 'otras_rrss')

#CRUD OFERTAS
class CrearOfertaForm(forms.ModelForm):
    class Meta:
        model = Oferta
        fields = ('descripcion', 'descripcion', 'requisitos', 'plataformas', 'otra_plataforma', 'fecha_expiracion' ) #[] antes
        widgets = {
                'fecha_expiracion': forms.DateInput(format='%Y-%m-%d',attrs={'type': 'date'}),
            }

