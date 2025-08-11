from django.shortcuts import render
from apps.noticias.models import Post

def inicio_view(request):
    posts = Post.objects.all().order_by("-created_at")[:6]
    return render(request, "inicio.html", {"posts": posts})

