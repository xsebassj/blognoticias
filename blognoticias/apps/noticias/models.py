from django.db import models
import uuid, os 
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify

class Category(models.Model):
    titulo = models.CharField(max_length=50)

    def __str__(self):
        return self.titulo
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
            self.slug =self.generate_unique_slug()
            super().save(*args, **kwargs)
        if not self.images.exists():
            PostImage.objects.created(post=self, image='noticias/default/post_default.png')
    

    def generate_unique_slug(self):
        slug = slugify(self.titulo)
        unique_slug= slug
        num= 1
        while Post.objects.filter(slug=unique_slug).exists():
            unique_slug= f'{slug}-{num}'
            num +=1
   


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False )
    autor = models.ForeignKey(settings.AUTH_USER_MODEL,  on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE , related_name= 'comments')
    contenido = models.TextField(max_length= 300)
    created_at = models.DateTimeField(default=timezone.now)
    update_at = models.DateTimeField(auto_now=True)



    def __str__(self):
        return self.titulo
    
   

class like(models.Model):
       autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name= 'likes')
       noticia  = models.ForeignKey(Post, on_delete=models.CASCADE)
       fecha = models.DateTimeField(default=timezone.now)

       class meta():
           unique_together= ('noticia', 'autor')
        
       def __str__(self):
         return f'{self.autor} le dio like a {self.noticia.titulo}'
    
def get_image_filename(instance, filename):
    post_id = instance.post.id
    image_count = instance.post.images.count()
    base_filemame , file_extension = os.path.splitext(filename)
    new_filename = f'pos_{post_id}_image{image_count + 1}{file_extension}'

    return os.path.join('noticias/cover/',new_filename)

@property
def amount_images(self):
    return self.images.count()
class PostImage(models.Model):
    post=models.ForeignKey(Post, on_delete=models.CASCADE, related_name= 'images')
    image = models.ImageField(upload_to=get_image_filename)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'PostImage {self.id}'
    
