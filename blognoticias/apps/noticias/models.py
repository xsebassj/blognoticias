from django.db import models
from usuarios.models import Persona
from django.utils import timezone

# Create your models here.


class Noticia(models.Model):
    autor = models.ForeignKey(Persona, on_delete=models.CASCADE)
    titulo = models.CharField(max_length= 100, blank=False , null=False)
    contenido = models.TextField()
    fecha_publicacion = models.DateTimeField(auto_now_add= True)
    imagen = models.ImageField ( upload_to='',blank=True,null= True)

    def __str__(self):
        return self.titulo

class Comentario(models.Model):
    noticia = models.ForeignKey(Noticia, on_delete=models.CASCADE, related_name= 'comentarios')
    autor = models.ForeignKey(Persona, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha_publicado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'comentario de {self.autor} en "{self.noticia.titulo}"'
    
