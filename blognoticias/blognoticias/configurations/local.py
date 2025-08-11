from .base import * 
from decouple import config,Csv
DEBUG = True
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

DATABASES = os.getenv('DJANGO_DATABASE')
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
