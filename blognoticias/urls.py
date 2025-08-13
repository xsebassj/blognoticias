"""
URL configuration for blognoticias project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import inicio_view
from django.contrib.staticfiles.views import serve
from django.views.generic.base import RedirectView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', inicio_view, name='inicio'),
    path('noticias/', include(('apps.noticias.urls', 'noticias'), namespace='noticias')),
    path('auth/', include(('apps.blog_auth.urls', 'blog_auth'), namespace='blog_auth')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += [

    path('favicon.ico', serve, {'path': 'assets/favicon.ico', 'document_root': settings.STATICFILES_DIRS[0]}),


    path('favicon.ico', RedirectView.as_view(url='/static/assets/favicon.ico')),
]