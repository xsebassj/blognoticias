from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SingUpForm(UserCreationForm):
    class meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class RegisterForm():
    class meta:
        model = User
        fields =['nombre','apellido','username','avatar','email']
        