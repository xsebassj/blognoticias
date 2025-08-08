from .base import * 

DEBUG = False

ALLOWED_HOSTS = ['production.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}