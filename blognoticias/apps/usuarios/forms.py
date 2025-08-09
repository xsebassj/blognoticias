from django import forms 
from .models import Persona, Perfil


class PersonaForm(forms.ModelForm):
    class meta:
        model = Persona
        fields = ['nombre', 'apellido']

class PerfilForm(forms.ModelForm):
    class meta:
        model = Perfil
        fields = ['biografia']