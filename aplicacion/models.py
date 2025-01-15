from django.db import models
from django.forms import ValidationError
from django.contrib.auth.models import User

# Create your models here.

#class Usuario(User):
    #nombre = models.CharField(max_length=50, verbose_name= 'Nombre de usuario')
    #email = models.EmailField()
    #preguntar JI


class Oferta(models.Model):
    PLATAFORMA_OPCIONES = [
                ('tiktok', 'TikTok' ),
                ('ig', 'Instagram' ),
                ('fb', 'Facebook' ),
                ('otra', 'Otra' ),
    ]

    ESTADO_OPCIONES = [
        ('vig', 'Vigente' ),
        ('exp', 'Expirada' ),
    ]
    #ID_OFERTA
    #empresa_id = models.ForeigKey[...]

    descripcion = models.TextField()
    requisitos = models.TextField()
    

    plataformas = models.CharField(max_length=50, choices = PLATAFORMA_OPCIONES)
    otra_plataforma = models.CharField(max_length=100,
                                        blank=True,  null=True )
    
    fecha_publicacion = models.DateField()
    fecha_expiracion = models.DateField()

    
    

class TipoDeOferta(models.Model):

    OFERTA_OPCIONES = [
                ('gastro', 'Gastronomía' ),
                ('moda', 'Moda' ),
                ('hogar', 'Hogar' ),
                ('tecnologia', 'Tecnología' ),
                ('eventos', 'Eventos' ),
                ('otra', 'Otro' ),
    ]

    oferta_id = models.ForeignKey(Oferta, on_delete=models.CASCADE, related_name="ofertas")

    tipo = models.CharField(max_length=100, choices=OFERTA_OPCIONES, verbose_name='Tipo de oferta')

    class Meta:
        verbose_name = 'Tipo de oferta'
        verbose_name_plural = 'Tipos de ofertas'

    def __init__(self):
        return f'Tipo de oferta: {self.tipo}'

    
class AplicacionOferta(models.Model):

    ESTADO_APLICACION_OFERTA = [
        ('aceptada', 'Aceptada'),
        ('denegada', 'Denegada'),
        ('solicitada', 'Solicitada'),
    ]

    RANGO_PUNTUACION = [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    ]

    #usuario_id
    oferta_id = models.ForeignKey(Oferta, on_delete=models.CASCADE, related_name="oferta_aplicada")
    estado_aplicacion = models.CharField(max_length=100, choices=ESTADO_APLICACION_OFERTA, verbose_name='Estado de la aplicación a la oferta')
    fecha_expiracion = models.DateField()
    puntuacion = models.CharField(max_length=10, choices=RANGO_PUNTUACION, blank=True, null=True)

    #FUNCION CLEAN PARA VALIDAR QUE SI ESTÁ LA OFERTA HECHA SE PUEDE PUNTUAR
   


    class Meta:
        verbose_name = 'Aplicación a la oferta'
        verbose_name_plural = 'Aplicaciones a las ofertas'

    def __init__(self):
        return f'Estado de la oferta: {self.estado_aplicacion}'