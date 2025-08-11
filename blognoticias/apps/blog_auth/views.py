from django.contrib.auth import authenticate, login,logout
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from .forms import RegisterForm,PerfilForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

User = get_user_model()

def Register_View(request):
    if request.user.is_authenticated:
        return redirect('inicio')  

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) 
            return redirect('inicio')
        else:
            print("Errores del formulario:", form.errors)
    else:
        form = RegisterForm()

    return render(request, 'blog_auth/register.html', {'form': form})


def Login_view(request):
    if request.user.is_authenticated:
        return redirect('inicio') 

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('inicio')
        else:
            print("Usuario o contraseña incorrectos")
    return render(request, 'blog_auth/login.html')



def logout_view(request):
    logout(request)
    messages.success(request, "Sesión cerrada correctamente.")
    return redirect('inicio')

@login_required
def perfil_view(request):
    user = request.user
    if request.method == 'POST':
        form = PerfilForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil actualizado correctamente.")
            return redirect('blog_auth:perfil')
    else:
        form = PerfilForm(instance=user)
    return render(request, 'blog_auth/perfil.html', {'form': form})

def about_site_view(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        email = request.POST.get("email")
        mensaje = request.POST.get("mensaje")

        # Validación básica
        if nombre and email and mensaje:
            print(f"📨 Nuevo mensaje de {nombre} ({email}): {mensaje}")
            messages.success(request, " ¡Gracias por tu mensaje! Te responderemos pronto.")
        else:
            messages.warning(request, " Todos los campos son obligatorios.")

    return render(request, 'blog_auth/about.html')