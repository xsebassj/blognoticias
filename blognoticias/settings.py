import os


env = os.getenv('DJANGO_ENV', 'local')

if env == 'production':
    from blognoticias.configurations.production import *
elif env == 'local':
    from blognoticias.configurations.local import *
else:
    from blognoticias.configurations.base import *