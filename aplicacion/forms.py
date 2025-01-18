from datetime import date
from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model



class CrearOfertaForm(forms.ModelForm):
    class Meta:
        model = Oferta
        fields = '__all__'
        widgets = {
                'fecha_expiracion': forms.DateInput(format='%Y-%m-%d',attrs={'type': 'date'}),
                'fecha_publicacion': forms.DateInput(format='%Y-%m-%d',attrs={'type': 'date'})
            }

class UsuarioParticularCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'biografia', 'foto_perfil', 'rol', 'instagram', 'tiktok', 'otras_rrss')
    
class UsuarioEmpresaCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'biografia', 'foto_perfil', 'rol')

class UsuarioActualizarPerfilForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'biografia', 'foto_perfil', 'rol', 'instagram', 'tiktok', 'otras_rrss')