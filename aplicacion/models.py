from django.db import models
from django.forms import ValidationError
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Usuario(AbstractUser):
    ROLES = [
        ('EMPRESA', 'Empresa'),
        ('PARTICULAR', 'Particular'),
    ]

    
    email = models.EmailField(unique=True)
    biografia = models.TextField(blank=True, null=True)
    foto_perfil = models.ImageField(upload_to='fotos_perfil/', blank=True, null=True)
    rol = models.CharField(max_length=10, choices=ROLES, default='PARTICULAR')
    instagram = models.CharField(max_length=150, blank=True, null=True)
    tiktok = models.CharField(max_length=150, blank=True, null=True)
    otras_rrss = models.CharField(max_length=100, blank=True, null=True)
    num_trabajos = models.PositiveIntegerField(default=0, blank=True, null=True)
    puntuacion_promedio = models.FloatField(default=0.0, blank=True, null=True)

   
    def __str__(self):
        return f"{self.username}"
        #{self.get_rol_display()}: {self.nombre}

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
    
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="ofertas")
    descripcion = models.TextField()
    requisitos = models.TextField()
    

    plataformas = models.CharField(max_length=50, choices = PLATAFORMA_OPCIONES)
    otra_plataforma = models.CharField(max_length=100, blank=True,  null=True ) #Con JS esconder este campo si no se escoge otra
    
    fecha_publicacion = models.DateField(auto_now_add=True)
    fecha_expiracion = models.DateField()

    def __str__(self):
        return f'oferta publicada por {self.usuario}'

    def clean(self):
        if self.fecha_expiracion <= self.fecha_publicacion:
            raise ValidationError("La fecha de expiración debe ser posterior a la fecha de publicación.")

    
    

class TipoDeOferta(models.Model):

    OFERTA_OPCIONES = [
                ('gastro', 'Gastronomía' ),
                ('moda', 'Moda' ),
                ('hogar', 'Hogar' ),
                ('tecnologia', 'Tecnología' ),
                ('eventos', 'Eventos' ),
                ('otra', 'Otro' ),
    ]

    oferta = models.ForeignKey(Oferta, on_delete=models.CASCADE, related_name="tiposDeOferta")

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

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="aplicacionesOferta")
    oferta = models.ForeignKey(Oferta, on_delete=models.CASCADE, related_name="aplicaciones")
    estado_aplicacion = models.CharField(max_length=100, choices=ESTADO_APLICACION_OFERTA, verbose_name='Estado de la aplicación a la oferta')
    fecha_expiracion = models.DateField()
    puntuacion = models.CharField(max_length=10, choices=RANGO_PUNTUACION, blank=True, null=True)

    class Meta:
        verbose_name = 'Aplicación a la oferta'
        verbose_name_plural = 'Aplicaciones a las ofertas'

    def __str__(self):
        return f'Estado de la oferta: {self.estado_aplicacion} | Fecha de expiración: {self.fecha_expiracion}'