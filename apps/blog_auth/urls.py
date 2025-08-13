from django.urls import path
from .views import (
    Register_View,
    Login_view,
    logout_view,
    perfil_view,
    about_site_view,
    Bandeja_view,
    Enviados_view,
    Enviar_view,
)

app_name = "blog_auth"

urlpatterns = [

    path('register/', Register_View, name='register'),
    path('login/', Login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('perfil/', perfil_view, name='perfil'),
    path('about/', about_site_view, name='about_site'),
    path("mensajes/", Bandeja_view, name="bandeja"),
    path("mensajes/enviados/", Enviados_view, name="enviado"),
    path("mensajes/enviar/", Enviar_view, name="enviar")
]
