from datetime import date
from django.db import models
from django.forms import ValidationError
from django.contrib.auth.models import AbstractUser
from django.http import HttpResponseForbidden

#USUARIOS
class Usuario(AbstractUser):
    ROLES = [
        ('EMPRESA', 'Empresa'),
        ('PARTICULAR', 'Particular'),
    ]

    
    email = models.EmailField(unique=True)
    biografia = models.TextField(blank=True, null=True)
    foto_perfil = models.ImageField(upload_to='fotos_perfil/', default='fotos_perfil/default.png')
    rol = models.CharField(max_length=10, choices=ROLES, default='PARTICULAR')
    num_trabajos = models.PositiveIntegerField(default=0, blank=True, null=True)
    puntuacion_promedio = models.DecimalField(default=0.0, max_digits=3,decimal_places=2, blank=True, null=True)

   
    def __str__(self):
        return f"{self.username}"
    
    def es_empresa(self):
        if self.rol == 'EMPRESA':
            return self.rol
        else:
            return 'No es empresa'
    
    

class RedesSocialesUsuario(models.Model):

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="get_usuario_redes")
    instagram = models.CharField(max_length=100, blank=True,  null=True)
    tiktok = models.CharField(max_length=100, blank=True,  null=True)
    youtube = models.CharField(max_length=100, blank=True,  null=True)
    twicht = models.CharField(max_length=100, blank=True,  null=True)



        
#OFERTAS
class Oferta(models.Model):

    ESTADO_OPCIONES = [
        ('vigente', 'Vigente' ),
        ('expirada', 'Expirada' ),
    ]

   
    
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="get_usuario_ofertas")
    tiktok = models.BooleanField(default=False)
    instagram = models.BooleanField(default=False)
    youtube = models.BooleanField(default=False)
    twitch = models.BooleanField(default=False)
    descripcion = models.TextField()
    requisitos = models.TextField()
    estado = models.CharField(max_length=50, choices=ESTADO_OPCIONES, default='vigente')
    fecha_publicacion = models.DateField(auto_now_add=True)
    fecha_expiracion = models.DateField()

    def __str__(self):
        return f'oferta publicada por {self.usuario}'
    
    def clean(self):
        if self.fecha_expiracion < date.today():
            raise ValidationError('ERROR: La fecha de expiración no puede ser anterior a hoy.')
    
    

    
  
class TipoDeOferta(models.Model):

    OFERTA_OPCIONES = [
                ('gastro', 'Gastronomía' ),
                ('moda', 'Moda' ),
                ('hogar', 'Hogar' ),
                ('tecnologia', 'Tecnología' ),
                ('eventos', 'Eventos' ),
                ('otra', 'Otro' ),
    ]

    oferta = models.ForeignKey(Oferta, on_delete=models.CASCADE, related_name="get_oferta_tipos")

    tipo = models.CharField(max_length=100, choices=OFERTA_OPCIONES, verbose_name='Tipo de oferta')



    class Meta:
        verbose_name = 'Tipo de oferta'
        verbose_name_plural = 'Tipos de ofertas'

    def __str__(self):
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

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="get_usuario_aplicaciones")

    oferta = models.ForeignKey(Oferta, on_delete=models.CASCADE, related_name="get_oferta_aplicaciones")

    estado_aplicacion = models.CharField(max_length=100, choices=ESTADO_APLICACION_OFERTA,
                                         default='solicitada',verbose_name='Estado de la aplicación a la oferta')
    
    fecha_expiracion = models.DateField(blank=True, null=True)

    puntuacion = models.CharField(max_length=10, choices=RANGO_PUNTUACION, blank=True, null=True)

    trabajo_puntuado = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Aplicación a la oferta'
        verbose_name_plural = 'Aplicaciones a las ofertas'

    def __str__(self):
        return f'Estado de la oferta: {self.estado_aplicacion} | Fecha de expiración: {self.fecha_expiracion}'