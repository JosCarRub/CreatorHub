from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'),

    #OFERTA
    path('oferta_form/', CrearOferta.as_view(), name='oferta_form'),
]