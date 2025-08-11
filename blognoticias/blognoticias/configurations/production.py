from .base import * 

DEBUG = os.getenv('DJANGO_DEBUG')

ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS')

DATABASES = os.getenv('DJANGO_DATABASE')