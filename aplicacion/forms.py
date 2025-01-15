from datetime import date
from django import forms
from .models import *

class CrearOfertaForm(forms.ModelForm):
    class Meta:
        model = Oferta
        fields = '__all__'
        widgets = {
                'fecha_expiracion': forms.DateInput(format='%Y-%m-%d',attrs={'type': 'date'}),
                'fecha_publicacion': forms.DateInput(format='%Y-%m-%d',attrs={'type': 'date'})
            }

#HACER MIGRACIONES INICIALES