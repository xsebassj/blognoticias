from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, PerfilForm
import logging

logger = logging.getLogger(__name__)
User = get_user_model()

def Register_View(request):
    if request.user.is_authenticated:
        return redirect('inicio')

    form = RegisterForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registro exitoso. ¡Bienvenido!")
            return redirect('inicio')
        else:
            logger.warning(f"Errores en registro: {form.errors}")
            messages.error(request, "Por favor corrige los errores del formulario.")
    return render(request, 'blog_auth/register.html', {'form': form})


def Login_view(request):
    if request.user.is_authenticated:
        return redirect('inicio')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        if not username or not password:
            messages.warning(request, "Usuario y contraseña son obligatorios.")
        else:
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f"Bienvenido, {user.username}!")
                return redirect('inicio')
            else:
                logger.info(f"Intento de login fallido para usuario: {username}")
                messages.error(request, "Usuario o contraseña incorrectos.")
    return render(request, 'blog_auth/login.html')


def logout_view(request):
    logout(request)
    messages.success(request, "Sesión cerrada correctamente.")
    return redirect('inicio')


@login_required
def perfil_view(request):
    user = request.user
    form = PerfilForm(request.POST or None, request.FILES or None, instance=user)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil actualizado correctamente.")
            return redirect('blog_auth:perfil')
        else:
            messages.error(request, "Error al actualizar el perfil.")
    return render(request, 'blog_auth/perfil.html', {'form': form})


def about_site_view(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre", "").strip()
        email = request.POST.get("email", "").strip()
        mensaje = request.POST.get("mensaje", "").strip()

        if nombre and email and mensaje:
            logger.info(f"📨 Mensaje recibido de {nombre} ({email}): {mensaje}")
            messages.success(request, "¡Gracias por tu mensaje! Te responderemos pronto.")
        else:
            messages.warning(request, "Todos los campos son obligatorios.")
    return render(request, 'blog_auth/about.html')
