from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from apps.noticias.models import Post, PostImage, Comment, Like, Category
from django.conf import settings
from apps.noticias.forms import PostFilterForm, PostCreateForm, CommentForm, PostForm, PostImageFormSet
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, render, redirect
from django.core.files import File
import os, uuid
from django.utils.text import slugify
from django.contrib import messages
from django.views import View


class PostListView(ListView):
    model = Post
    template_name = 'noticias/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = Post.objects.all()

        categoria_id = self.request.GET.get('categoria')
        if categoria_id:
            queryset = queryset.filter(category_id=categoria_id)

        orden = self.request.GET.get('orden', 'reciente')
        if orden == 'reciente':
            queryset = queryset.order_by('-created_at')
        elif orden == 'antiguo':
            queryset = queryset.order_by('created_at')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Category.objects.all()
        context['categoria_seleccionada'] = self.request.GET.get('categoria')
        return context


class PostCreateView(CreateView):
    model = Post
    form_class = PostCreateForm
    template_name = "noticias/post_create.html"
    success_url = reverse_lazy("noticias:posts")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.all()
        return context

    def form_valid(self, form):
        form.instance.autor = self.request.user
        post = form.save()

        images = self.request.FILES.getlist("images")
        default_path = getattr(settings, 'DEFAULT_POST_IMAGE_PATH', None)

        if not post.images.exists():
            if images and any(img.size > 0 for img in images):
                for image in images:
                    PostImage.objects.create(post=post, image=image)
            elif default_path and os.path.exists(str(default_path)):
                with open(default_path, "rb") as f:
                    default_image = File(f)
                    PostImage.objects.create(post=post, image=default_image)
            else:
                print("⚠ Imagen por defecto no encontrada o no definida.")

        self.object = post
        messages.success(self.request, "✅ ¡Publicación creada con éxito!")
        return super().form_valid(form)


class PostDetailView(DetailView):
    model = Post
    template_name = "noticias/post_detail.html"
    context_object_name = "post"

    def get_object(self):
        slug = self.kwargs.get("slug")
        return get_object_or_404(Post, slug=slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        user = self.request.user
        active_images = post.images.filter(active=True)

        context["active_images"] = active_images
        context["add_comment_form"] = CommentForm()
        context["likes_count"] = post.like_set.count()
        context["comment_form"] = CommentForm()
        context["has_images"] = active_images.exists()
        context["liked_by_user"] = post.like_set.filter(autor=user).exists() if user.is_authenticated else False

        edit_comment_id = self.request.GET.get("edit_comment")
        if edit_comment_id:
            comment = get_object_or_404(Comment, id=edit_comment_id)
            if comment.autor == user:
                context["editing_comment_id"] = comment.id
                context["edit_comment_form"] = CommentForm(instance=comment)
            else:
                context["editing_comment_id"] = None
                context["edit_comment_form"] = None

        delete_comment_id = self.request.GET.get("delete_comment")
        if delete_comment_id:
            comment = get_object_or_404(Comment, id=delete_comment_id)
            if (
                comment.autor == user
                or (
                    comment.post.autor == user
                    and not comment.autor.is_admin
                    and not comment.autor.is_superuser
                )
                or user.is_superuser
                or user.is_staff
                or user.is_admin
            ):
                context["deleting_comment_id"] = comment.id
            else:
                context["deleting_comment_id"] = None

        return context


class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = "noticias/post_update.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.method == "POST":
            context['image_formset'] = PostImageFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            context['image_formset'] = PostImageFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        post = form.save(commit=False)
        nuevo_slug = slugify(post.titulo)

        if post.slug != nuevo_slug:
            post.slug = nuevo_slug

        post.save()
        self.object = post

        image_formset = PostImageFormSet(self.request.POST, self.request.FILES, instance=post)
        print("Formset válido:", image_formset.is_valid())
        print("Errores:", image_formset.errors)

        if image_formset.is_valid():
            image_formset.save()
        else:
            context = self.get_context_data(form=form)
            context['image_formset'] = image_formset
            return self.render_to_response(context)

        messages.success(self.request, "✅ Publicación actualizada con éxito.")
        return redirect(self.get_success_url())


class PostDeleteView(DeleteView):
    model = Post
    template_name = "noticias/post_delete.html"

    def delete(self, request, *args, **kwargs):
        messages.success(request, "🗑️ La publicación fue eliminada correctamente.")
        return super().delete(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.POST.get("confirm_delete") == "on":
            return super().post(request, *args, **kwargs)
        messages.error(request, "Debes confirmar que querés eliminar la publicación.")
        return redirect(self.object.get_absolute_url())

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.autor != request.user:
            return redirect(self.object.get_absolute_url())
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('noticias:posts')


class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "noticias/post_detail.html"

    def form_valid(self, form):
        form.instance.autor = self.request.user
        form.instance.post = Post.objects.get(slug=self.kwargs["slug"])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("noticias:post_detail", kwargs={"slug": self.object.post.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = Post.objects.get(slug=self.kwargs["slug"])
        context["post"] = post
        context["comments"] = post.comments.order_by("-created_at")
        return context


class CommentUpdateView(UpdateView):
    model = Comment
    fields = ['contenido']
    template_name = 'noticias/comment_update.html'

    def get_success_url(self):
        return self.object.post.get_absolute_url()

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.autor != request.user:
            return redirect(self.object.post.get_absolute_url())
        return super().dispatch(request, *args, **kwargs)


class CommentDeleteView(DeleteView):
    model = Comment
    template_name = 'noticias/comment_delete.html'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.autor != request.user:
            return redirect(self.object.post.get_absolute_url())
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        comment = self.get_object()
        return comment.post.get_absolute_url()

class LikeView(LoginRequiredMixin, View):
    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        like, created = Like.objects.get_or_create(autor=request.user, noticia=post)

        if not created:
            like.delete()
        return redirect(post.get_absolute_url())




class PostSearchView(ListView):
    model = Post
    template_name = 'noticias/search_results.html'
    context_object_name = 'resultados'

    def get_queryset(self):
      query = self.request.GET.get('q', '').strip()
      if query:
        return Post.objects.filter(
            Q(titulo__icontains=query) | Q(contenido__icontains=query)
        )
      return Post.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context

class PostPorCategoriaView(ListView):
    model = Post
    template_name = 'noticias/post_list.html'
    context_object_name = 'articulos'

    def get_queryset(self):
        self.categoria = get_object_or_404(Category, slug=self.kwargs['slug'])
        return Post.objects.filter(category=self.categoria).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.categoria
        context['categorias'] = Category.objects.all().order_by('name')
        return context

class CategoryListView(ListView):
    model = Category
    template_name = 'noticias/post_list.html'
    context_object_name = 'category'

class PostListView(ListView):
    model = Post
    template_name = 'noticias/post_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        queryset = Post.objects.all()

        categoria_id = self.request.GET.get('categoria')
        if categoria_id:
            queryset = queryset.filter(category_id=categoria_id)

        orden = self.request.GET.get('orden', 'reciente')
        if orden == 'reciente':
            queryset = queryset.order_by('-created_at')
        elif orden == 'antiguo':
            queryset = queryset.order_by('created_at')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Category.objects.all()
        context['categoria_seleccionada'] = self.request.GET.get('categoria')
        return context