from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'),

    #REGISTRO
    path('registro_particular/', RegistroParticularView.as_view(), name='registro_particular'),
    path('registro_empresa/', RegistroEmpresaView.as_view(), name='registro_empresa'),

    #PÁGINA PRINCIPAL
    path('principal/', PrincipalListadoOfertasView.as_view(), name='principal'),



    #PERFIL   
    path('perfil/', UsuarioPerfilView.as_view(), name='perfil'),
    path('perfil_actualizar/', UsuarioActualizarPerfilView.as_view(), name='perfil_actualizar'),
    path('perfil_borrar/', UsuarioBorrarPerfilView.as_view(), name='perfil_borrar'),
    #REDES
    path('perfil_completar_redes/', UsuarioCompletarRedesView.as_view(), name='perfil_completar_redes'),
    path('perfil_actualizar_redes/<int:pk>', UsuarioActualizarRedesView.as_view(), name='perfil_actualizar_redes'),


    


    #OFERTA
    path('crear_oferta/', CrearOfertaView.as_view(), name='crear_oferta'),
    path('detalle_oferta/<int:pk>', DetalleOfertaView.as_view(), name='detalle_oferta'),
    path('aplicar_oferta/<int:pk>', AplicarOfertaView.as_view(), name='aplicar_oferta'),
    #APLICACIONES
    path('detalle_aspirantes_oferta/<int:pk>', DetalleAspirantesOfertaView.as_view(), name='detalle_aspirantes_oferta'),
    path('puntuar_aspirante_oferta/<int:oferta_id>/<int:aplicacion_id>/', PuntuarAplicacionView.as_view(), name='puntuar_aspirante_oferta'),



    

     
    


]