from django.db import models

# Create your models here.


class usuario(models.Model):

    nombre= models.CharField(max_length=50, blank= False , null= False)
    apellido = models.CharField(max_length=50, blank= False , null= False)
    

    