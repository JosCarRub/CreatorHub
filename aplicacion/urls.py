from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'),

    #REGISTRO
    path('registro_particular/', RegistroParticularView.as_view(), name='registro_particular'),
    path('registro_empresa/', RegistroEmpresaView.as_view(), name='registro_empresa'),

    #PÁGINA PRINCIPAL
    path('principal/', PrincipalView.as_view(), name='principal'),


    #PERFIL
    path('perfil', UsuarioActualizarPerfil.as_view(), name='perfil'),
]