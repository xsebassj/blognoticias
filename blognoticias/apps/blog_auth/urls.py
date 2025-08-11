from django.urls import path
from .views import Register_View,Login_view,logout_view,perfil_view,about_site_view

app_name = "apps.blog_auth"

urlpatterns = [
    path('register/', Register_View, name = 'register' ),
    path('login/', Login_view, name = 'login' ),
    path('logout/', logout_view, name='logout'),
    path('perfil/', perfil_view, name='perfil'),
    path('about/', about_site_view, name='about_site'),
]
