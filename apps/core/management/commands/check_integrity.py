# blognoticias/apps/core/management/commands/check_integrity.py

import os
from django.core.management.base import BaseCommand
from django.conf import settings
from importlib import import_module

class Command(BaseCommand):
    help = "Verifica la integridad del entorno de producción"

    def handle(self, *args, **kwargs):
        self.stdout.write("🔍 Verificando entorno...")

        # 1. Verificar importación de settings
        try:
            prod = import_module('blognoticias.configurations.production')
            self.stdout.write("✅ settings.production importado correctamente")
        except Exception as e:
            self.stdout.write(f"❌ Error al importar settings.production: {e}")

        # 2. Verificar .env
        env_path = os.path.join(settings.BASE_DIR, '.env')
        if os.path.exists(env_path):
            self.stdout.write("✅ .env encontrado")
        else:
            self.stdout.write("⚠️ .env no encontrado")

        # 3. Verificar templates críticos
        templates_ok = True
        for tpl in ['base.html', 'error.html']:
            found = False
            for dir in settings.TEMPLATES[0]['DIRS']:
                if os.path.exists(os.path.join(dir, tpl)):
                    found = True
                    break
            if found:
                self.stdout.write(f"✅ Template '{tpl}' encontrado")
            else:
                self.stdout.write(f"❌ Template '{tpl}' no encontrado")
                templates_ok = False

        # 4. Verificar STATIC_ROOT
        if hasattr(settings, 'STATIC_ROOT') and settings.STATIC_ROOT:
            self.stdout.write(f"✅ STATIC_ROOT configurado: {settings.STATIC_ROOT}")
        else:
            self.stdout.write("⚠️ STATIC_ROOT no configurado")

        # 5. Verificar __init__.py en paquetes clave
        for path in ['blognoticias', 'blognoticias/configurations', 'apps']:
            init_path = os.path.join(settings.BASE_DIR, path, '__init__.py')
            if os.path.exists(init_path):
                self.stdout.write(f"✅ {path}/__init__.py presente")
            else:
                self.stdout.write(f"❌ Falta {path}/__init__.py")

        self.stdout.write("✅ Verificación completa")
