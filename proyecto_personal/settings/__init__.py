import os

ENV = os.getenv('DJANGO_ENV', 'local')  # Cambiar esta variable en producción

if ENV == 'local':
    from .local import *
else:
    from .production import *