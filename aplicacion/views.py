from django.shortcuts import render
from django.views.generic import ListView ,TemplateView
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class HomeView(TemplateView):
    template_name = 'home.html'