from django.shortcuts import render
from django.views.generic import ListView ,TemplateView, CreateView
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
from django.urls import reverse_lazy

# Create your views here.
class HomeView(TemplateView):
    template_name = 'home.html'

class CrearOferta(CreateView):
    model = Oferta
    template_name = 'oferta_form.html'
    form_class = CrearOfertaForm
    success_url = reverse_lazy('home')