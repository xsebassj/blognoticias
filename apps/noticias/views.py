from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.db.models import Count, Q
from apps.noticias.models import Post, PostImage, Comment, Like, Category
from apps.noticias.forms import  CommentForm, PostForm, PostImageFormSet
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, render, redirect
from django.core.files import File
from django.contrib import messages
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class CategoryListView(ListView):
    model = Category
    template_name = 'noticias/post_list.html'
    context_object_name = 'category'

class PostListView(ListView):
    model = Post
    template_name = 'noticias/post_list.html'
    context_object_name = 'posts'
    paginate_by= 10
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
        elif orden == "az":
            queryset = queryset.order_by("titulo")
        elif orden == "za":
            queryset = queryset.order_by("-titulo")

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Category.objects.all()
        context['categoria_seleccionada'] = self.request.GET.get('categoria')
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "noticias/post_create.html"

    def get_success_url(self):
        return reverse_lazy("noticias:post_detail", kwargs={"slug": self.object.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.POST:
            context["image_formset"] = PostImageFormSet(
                self.request.POST,
                self.request.FILES,
                instance=getattr(self, "object", Post())
            )
        else:
            context["image_formset"] = PostImageFormSet(instance=Post())

        context["category"] = Category.objects.all()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        image_formset = context["image_formset"]

        if form.is_valid() and image_formset.is_valid():
            self.object = form.save(commit=False)
            self.object.autor = self.request.user
            self.object.save()

            uploaded_images = [
                f for f in image_formset
                if f.cleaned_data.get('image')
                and not f.cleaned_data.get('DELETE', False)
            ]
            if uploaded_images:
                image_formset.instance = self.object
                image_formset.save()
            else:
                PostImage.objects.create(
                    post=self.object,
                    image='noticias/default/post_default.png',
                    active=True
                )

            return super().form_valid(form)

        return self.form_invalid(form)

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
        context.update({
            "active_images": active_images,
            "has_images": active_images.exists(),
            "add_comment_form": CommentForm(),
            "comment_form": CommentForm(),
            "likes_count": post.like_set.count(),
            "liked_by_user": post.like_set.filter(autor=user).exists() if user.is_authenticated else False,
        })
        context["editing_comment_id"] = None
        context["edit_comment_form"] = None
        edit_comment_id = self.request.GET.get("edit_comment")
        if edit_comment_id and user.is_authenticated:
            comment = get_object_or_404(Comment, id=edit_comment_id)
            if comment.autor == user:
                context["editing_comment_id"] = comment.id
                context["edit_comment_form"] = CommentForm(instance=comment)

        context["deleting_comment_id"] = None
        delete_comment_id = self.request.GET.get("delete_comment")
        if delete_comment_id and user.is_authenticated:
            comment = get_object_or_404(Comment, id=delete_comment_id)
            can_delete = (
                comment.autor == user
                or (comment.post.autor == user and not getattr(comment.autor, "is_admin", False) and not getattr(comment.autor, "is_superuser", False))
                or user.is_superuser
                or user.is_staff
                or getattr(user, "is_admin", False)
            )
            if can_delete:
                context["deleting_comment_id"] = comment.id

        return context


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "noticias/post_update.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_success_url(self):
        return reverse_lazy("noticias:post_detail", kwargs={"slug": self.object.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["image_formset"] = PostImageFormSet(
                self.request.POST,
                self.request.FILES,
                instance=self.object
            )
        else:
            context["image_formset"] = PostImageFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        image_formset = context["image_formset"]

        if image_formset.is_valid():
            self.object = form.save()
            image_formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(context)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.autor or self.request.user.is_superuser

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
        can_delete = (
            request.user.is_superuser or
            self.object.autor == request.user
        )

        if not can_delete:
            messages.error(request, "No tienes permisos para eliminar esta publicación.")
            return redirect(self.object.get_absolute_url())

        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('noticias:posts')

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'noticias/comment_form.html'
    success_url = reverse_lazy('noticias:post_detail')

    def form_valid(self, form):
        post = get_object_or_404(Post, slug=self.kwargs["slug"])
        form.instance.autor = self.request.user
        form.instance.post = post
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("noticias:post_detail", kwargs={"slug": self.kwargs["slug"]})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = get_object_or_404(Post, slug=self.kwargs["slug"])
        context["post"] = post
        context["comments"] = post.comments.order_by("-created_at")
        context["add_comment_form"] = context.get("form", self.get_form())
        return context

class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'noticias/comment_update.html'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        can_edit = (
            request.user.is_superuser or
            self.object.autor == request.user
        )

        if not can_edit:
            messages.error(request, "No tienes permisos para editar este comentario.")
            return redirect(self.object.post.get_absolute_url())

        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):

        pk = self.kwargs.get("pk")
        comment = get_object_or_404(Comment, pk=pk)
        return comment

    def form_valid(self, form):
        messages.success(self.request, "✏️ El comentario fue actualizado correctamente.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("noticias:post_detail", kwargs={"slug": self.object.post.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object.post
        context["post"] = post
        context["comments"] = post.comments.order_by("-created_at")
        context["is_admin_edit"] = (
            self.request.user.is_superuser and
            self.request.user != self.object.autor
        )
        return context

class CommentDeleteView(DeleteView):
    model = Comment
    template_name = 'noticias/comment_delete.html'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        can_delete = (
            request.user.is_superuser or
            self.object.autor == request.user
        )

        if not can_delete:
            messages.error(request, "No tienes permisos para eliminar este comentario.")
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

