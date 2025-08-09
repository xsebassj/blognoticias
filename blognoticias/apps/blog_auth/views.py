from django.shortcuts import render, redirect
from .forms import SingUpForm
from django.contrib.auth import authenticate, login 
from django.contrib import messages
# Create your views here.

def Register_view(request):
    if request.method == "POST":
        form = SingUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("apps.blog_auth:login")
    else:
        form = SingUpForm()
    return render(request, "templates/blog_auth/register.html", {"form" : form}) 


def Login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('apps.blog_auth:login')
        else :
            messages.error(request, 'credenciales incorrectas')
    return render(request, 'blog_auth/login.html')
