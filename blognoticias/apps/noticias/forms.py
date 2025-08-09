from .models import Noticia,Comentario
from django import forms



class NoticiaForm(forms.ModelForm):
    class meta:
        model = Noticia
        fields =['titulo','contenido','imagen']

class ComentarioForm(forms.ModelForm):
    class meta:
        model = Comentario
        fields = ['contenido']