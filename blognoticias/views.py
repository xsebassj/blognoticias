from django.shortcuts import render
from apps.noticias.models import Post
import logging
import traceback

logger = logging.getLogger(__name__)

def inicio_view(request):
    context = {}
    try:
        posts = Post.objects.all()
        context['posts'] = posts
        return render(request, "inicio.html", context)
    except Exception as e:
        logger.error(f"[inicio_view] {type(e).__name__}: {e}")
        logger.debug(traceback.format_exc())
        context['error'] = "Ocurrió un error al cargar las noticias."
        return render(request, "error.html", context)
