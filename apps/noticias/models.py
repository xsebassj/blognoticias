from django.db import models
import uuid, os
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify
from django.core.files import File
from pathlib import Path
from django.urls import reverse





class Category(models.Model):
    titulo = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return self.titulo

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,null=True, related_name= 'post')
    titulo = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=100 , blank=True, null=True)
    contenido = models.TextField()
    autor = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    update_at = models.DateTimeField(auto_now=True)
    allow_comments = models.BooleanField(default=True)
    def __str__(self):
        return self.titulo

    @property
    def amount_comments(self):
        return self.comments.count()

    def save(self, *args, **kwargs):
      if not self.slug:
        self.slug = self.generate_unique_slug()

      is_new = self._state.adding
      super().save(*args, **kwargs)
    def get_absolute_url(self):
        return reverse("noticias:post_detail", kwargs={"slug": self.slug})

    def generate_unique_slug(self):
        slug = slugify(self.titulo)
        unique_slug= slug
        num= 1
        while Post.objects.filter(slug=unique_slug).exists():
            unique_slug= f'{slug}-{num}'
            num +=1
        return unique_slug
    @property
    def amount_images(self):
        return self.images.count()



class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False )
    autor = models.ForeignKey(settings.AUTH_USER_MODEL,  on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE , related_name= 'comments')
    contenido = models.TextField(max_length= 300)
    created_at = models.DateTimeField(default=timezone.now)
    update_at = models.DateTimeField(auto_now=True)



    def __str__(self):
        return f'Comentario de {self.autor} en {self.post.titulo}'



class Like(models.Model):
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='likes')
    noticia = models.ForeignKey(Post, on_delete=models.CASCADE)
    fecha = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('noticia', 'autor')

    def __str__(self):
        return f'{self.autor} le dio like a {self.noticia.titulo}'
    def get_context_data(self, **kwargs):
     context = super().get_context_data(**kwargs)
     context["liked_by_user"] = self.object.like_set.filter(autor=self.request.user).exists()
     context["likes_count"] = self.object.like_set.count()
     return context

def get_image_filename(instance, filename):
    post_id = instance.post.id if instance.post else 'unknown'
    unique_id = uuid.uuid4().hex[:8]
    base_filename, file_extension = os.path.splitext(filename)
    new_filename = f'post_{post_id}_{unique_id}{file_extension}'
    return os.path.join('noticias/cover/', new_filename)

class PostImage(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(
        upload_to=get_image_filename,
        default='noticias/default/post_default.png'
    )
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Imagen para {self.post.titulo}"


