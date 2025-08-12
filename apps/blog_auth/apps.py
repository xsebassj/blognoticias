from django.apps import AppConfig


class BlogAuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.blog_auth'

def ready(self):
    import apps.blog_auth.signals