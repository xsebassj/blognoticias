from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid,os



def get_avatar_filename(instance, filename):
    base_filename, file_extension = os.path.splitext(filename)
    new_filename = f"user_{instance.id}_avatar{file_extension}"
    return os.path.join("usuarios/avatar/",new_filename)

     
# Create your models here.

class user(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre_usuario = models.CharField(max_length=20, blank=False,null=False)
    avatar = models.ImageField(upload_to=get_avatar_filename, default='usuario/default/avatar_default.jpg')
    email = models.EmailField()
    
    
    def __str__(self):
      return self.username


@property
def is_collaborator(self):
   return self.groups.filter(name='collaborators').exist()
@property
def is_registered(self):
   return self.groups.filter(name='registered').exist()
@property
def is_admin(self):
   return self.groups.filter(name='admins').exist()