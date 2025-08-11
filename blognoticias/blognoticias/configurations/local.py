from .base import * 

DEBUG = True
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
