from django.db import models
import uuid, os
from django.conf import settings
from django.utils import timezone


class post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    titulo = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=100 , blank=True, null=True)
    contenido = models.TextField()
    autor = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    update_at = models.DateTimeField(auto_now=True)

    

