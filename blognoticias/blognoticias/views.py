from django.shortcuts import render
from apps.noticias.models import Post
import logging

logger = logging.getLogger(__name__)

def inicio_view(request):
    try:
        posts = Post.objects.all()
        return render(request, "inicio.html", {"posts": posts})
    except Exception as e:
        logger.error(f"Error en inicio_view: {e}")
        return render(request, "error.html", {"error": str(e)})

