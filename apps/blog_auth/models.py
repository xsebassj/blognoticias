from django.db import models
from django.contrib.auth.models import AbstractUser,UserManager
import uuid,os


def get_avatar_filename(instance, filename):
    base_filename, file_extension = os.path.splitext(filename)
    new_filename = f"user_{instance.id}_avatar{file_extension}"
    return os.path.join("media/usuarios/avatar/",new_filename)


# Create your models here.

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=20, unique=True)
    avatar = models.ImageField(upload_to=get_avatar_filename, default='usuario/default/avatar_default.jpg')
    email = models.EmailField(unique=True)

    objects = UserManager()

    def __str__(self):
      return self.username


@property
def is_collaborator(self):
   return self.groups.filter(name='collaborators').exists()
@property
def is_registered(self):
   return self.groups.filter(name='registered').exists()
@property
def is_admin(self):
   return self.groups.filter(name='admins').exists()