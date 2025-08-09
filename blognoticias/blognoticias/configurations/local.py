from .base import * 

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

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
