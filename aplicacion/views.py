from django.shortcuts import render
from django.views.generic import ListView ,TemplateView, CreateView
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm


# Create your views here.
class HomeView(TemplateView):
    template_name = 'home.html'

class RegistroView(CreateView):
    form_class = UsuarioCreationForm
    template_name = 'registration/registro.html'
    success_url = reverse_lazy('login')