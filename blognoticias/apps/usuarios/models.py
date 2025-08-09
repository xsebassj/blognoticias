from django.db import models

# Create your models here.


class Persona(models.Model):

    nombre= models.CharField(max_length=50, blank= False , null= False)
    apellido = models.CharField(max_length=50, blank= False , null= False)
    def __str__(self):
        return f'{self.nombre} {self.apellido}'
    
class Perfil(models.Model):
    usuario = models.OneToOneField(Persona,on_delete=models.CASCADE)
    biografia = models.TextField()

    
    
