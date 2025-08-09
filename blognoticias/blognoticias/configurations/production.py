from .base import * 

DEBUG = False

ALLOWED_HOSTS = ['production.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'blognoticias',
        'USER': 'bloguser',
        'PASSWORD': 'sebas312',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}