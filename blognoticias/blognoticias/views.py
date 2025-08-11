from django.shortcuts import render
from apps.noticias.models import Post

def inicio_view(request):
    posts = Post.objects.all().order_by("-created_at")[:6]
    return render(request, "inicio.html", {"posts": posts})

from django.http import HttpResponse

def home(request):
    return HttpResponse("¡Hola Sebas! Django está vivo y respondiendo.")
