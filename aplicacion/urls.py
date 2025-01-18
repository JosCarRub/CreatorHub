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
    path('perfil/', UsuarioPerfilView.as_view(), name='perfil'),
    path('perfil_actualizar/', UsuarioActualizarPerfilView.as_view(), name='perfil_actualizar'),
    path('perfil_borrar/', UsuarioBorrarPerfilView.as_view(), name='perfil_borrar'),

    #OFERTA
    path('crear_oferta/', CrearOfertaView.as_view(), name='crear_oferta'),

]