from .base import * 

DEBUG = True

ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS')

DATABASES = os.getenv('DJANGO_DATABASE')