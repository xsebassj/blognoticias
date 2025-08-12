import os
import sys
from pathlib import Path

# Ruta base del proyecto (donde está manage.py)
PROJECT_ROOT = Path(__file__).resolve().parent / "blognoticias"
sys.path.insert(0, str(PROJECT_ROOT.parent))
# Cargar settings de producción
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blognoticias.configurations.production')

# Test de importación
import blognoticias.configurations.production
print("✅ Módulo importado correctamente")

# Test de WSGI
try:
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
    print("✅ WSGI cargado correctamente")
except Exception as e:
    print("❌ Error al cargar WSGI:")
    import traceback
    traceback.print_exc()

# Test de settings
from django.conf import settings
print("DEBUG:", settings.DEBUG)
print("ALLOWED_HOSTS:", settings.ALLOWED_HOSTS)
print("BASE_DIR:", settings.BASE_DIR)