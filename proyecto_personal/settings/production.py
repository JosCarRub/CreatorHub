from .base import *
DEBUG = False
ALLOWED_HOSTS = ['localhost']


DATABASES = {
     'default': {
         'ENGINE': 'mysql.connector.django',  # Motor para mysql-connector-python
         'NAME': config['database']['name'],  # Nombre de la base de datos
         'USER': config['database']['user'],                # Usuario de la base de datos
         'PASSWORD': config['database']['password'],         # Contraseña del usuario
         'HOST': config['database']['host'],                # Dirección del servidor
         'PORT': config['database']['port'],
         'OPTIONS': {
             'autocommit': True,
             'charset': 'utf8mb4',
         },                                        
     }
}