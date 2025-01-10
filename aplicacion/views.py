from django.shortcuts import render
from django.views.generic import ListView ,TemplateView
from .models import *

# Create your views here.
class HomeView(TemplateView):
    template_name = 'home.html'