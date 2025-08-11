from .base import * 
DEBUG = False

ALLOWED_HOSTS = ['xsebasssj.pythonanywhere.com']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'blognoticias_db',
        'USER': 'sebas',
        'PASSWORD': 'tu_contraseña_segura',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}


STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
SECURE_HSTS_SECONDS = 3600
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
