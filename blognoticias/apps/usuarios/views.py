from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

# creando views

def signup(request):
    return render(request, 'templates/usuarios/signup.html',
                  form = UserCreationForm)
