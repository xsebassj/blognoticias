from django import forms  
from apps.noticias.models import Comment, Post, PostImage,Category
from django.forms import inlineformset_factory
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('titulo', 'contenido', 'allow_comments')

class PostFilterForm(forms.Form):
    searche_query = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'buscar...', 'class': 'w-full p-2'}))

    order_by = forms.ChoiceField(
    required=False,
    choices=(
        ('-created_at', 'Más recientes'),
        ('created_at', 'Más antiguos'),
        ('-comments_count', 'Más comentados'),
    ),
    widget=forms.Select(attrs={'class': 'w-full p-2'})
)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment

        fields = ['contenido']

        labels = {
            'contenido':  'Comentario'
        }

        widgets = {
            'contenido': forms.Textarea(
                attrs={
                    'rows': 3, 'placeholder': 'Escribe tu comentario...', 'class': 'p-2'
                }
            )
        }

class PostCreateForm(PostForm):
    def save(self, commit=True):
        post = super().save(commit=False)
        if commit:
            post.save()
        return post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['titulo', 'contenido', 'category']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
        }
        

class PostImageForm(forms.ModelForm):
    image = forms.ImageField(required=False)

    class Meta:
        model = PostImage
        fields = ['image', 'active']

PostImageFormSet = inlineformset_factory(
    Post,
    PostImage,
    form=PostImageForm,
    extra=0,
    can_delete=True
)