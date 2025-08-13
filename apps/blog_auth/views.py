from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, PerfilForm, MensajeForm
import logging
from .models import Mensajes

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

    if request.method == 'POST':
        form = PerfilForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil actualizado correctamente.")
            return redirect('blog_auth:perfil')
        else:
            messages.error(request, "Error al actualizar el perfil. Revisa los datos.")
    else:
        form = PerfilForm(instance=user)
    return render(request, 'blog_auth/perfil.html', {'form': form})




def about_site_view(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre", "").strip()
        email = request.POST.get("email", "").strip()
        mensaje = request.POST.get("mensaje", "").strip()

        if not nombre or not email or not mensaje:
            messages.warning(request, "Todos los campos son obligatorios.")
        elif "@" not in email or "." not in email:
            messages.warning(request, "Por favor, ingresa un correo electrónico válido.")
        else:
            logger.info(f"📨 Mensaje recibido de {nombre} ({email}): {mensaje}")
            messages.success(request, "¡Gracias por tu mensaje! Te responderemos pronto.")
            return redirect("blog_auth:about_site")
    return render(request, 'blog_auth/about.html')


@login_required
def Bandeja_view(request):
    mensaje_b = Mensajes.objects.filter(destinatario=request.user).select_related("emisor")
    return render(request, "blog_auth/bandeja.html", {"mensajes": mensaje_b})

@login_required
def Enviados_view(request):
    mensaje_c = Mensajes.objects.filter(emisor=request.user).select_related("destinatario")
    return render(request, "blog_auth:enviado.html",{"mensajes": mensaje_c})

@login_required
def Enviar_view(request):
    if request.method == "POST":
        form = MensajeForm(request.POST)
        if form.is_valid():
            mensaje = form.save(commit=False)
            mensaje.emisor = request.user
            mensaje.save()
            return redirect("blog_auth:bandeja")
    else:
        form = MensajeForm()
    return render(request, "blog_auth/enviar.html", {"form": form})
