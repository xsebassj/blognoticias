from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms

User = get_user_model()
class SingUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class RegisterForm():
    class Meta:
        model = User
        fields =['nombre','apellido','username','avatar','email']

class PerfilForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'avatar']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }        