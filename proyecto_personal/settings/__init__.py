import os

ENV = os.getenv('DJANGO_ENV', 'local')  # Cambiar esta variable en producción

if ENV == 'local':
    from .production import *
else:
    from .local import *