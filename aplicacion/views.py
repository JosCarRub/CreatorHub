from django.shortcuts import render
from django.views.generic import ListView ,TemplateView, CreateView
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