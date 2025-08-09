from django.urls import path
from .views import Register_view,Login_view,logout_view

app_name = "apps.blog_auth"

urlpatterns = [
    path('register/', Register_view, name = 'register' ),
    path('login/', Login_view, name = 'login' ),
    path('logout/', logout_view, name='logout'),
]
