import os
import sys
from pathlib import Path

path = '/home/xsebasssj/blognoticias'
if path not in sys.path:
    sys.path.append(path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blognoticias.configurations.production')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()