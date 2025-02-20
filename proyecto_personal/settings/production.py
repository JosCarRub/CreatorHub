from .base import *
import yaml

DEBUG = True
ALLOWED_HOSTS = ['josecarloscr.ieshm.org']

BASE_DIR = Path(__file__).resolve().parent.parent.parent
with open(BASE_DIR / 'config.yaml') as f:
    config = yaml.safe_load(f)


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