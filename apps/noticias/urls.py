from django.urls import path
from .views import *
app_name = 'noticias'
urlpatterns = [

    path('posts/', PostListView.as_view(), name='posts'),
    path('create/', PostCreateView.as_view(), name='create'),
    path('detail/<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
    path("post/<slug:slug>/editar/", PostUpdateView.as_view(), name="post_update"),
    path("post/<slug:slug>/eliminar/", PostDeleteView.as_view(), name="post_delete"),
    path("post/<slug:slug>/comment/", CommentCreateView.as_view(), name="comment"),
    path('comment-up/<uuid:pk>/', CommentUpdateView.as_view(), name='comment_update'),
    path('comment-del/<uuid:pk>/', CommentDeleteView.as_view(), name='comment_delete'),
    path('post/<slug:slug>/like/', LikeView.as_view(), name='like'),
    path('buscar/', PostSearchView.as_view(), name='search'),
    path('categoria/<slug:slug>/', PostPorCategoriaView.as_view(), name='categoria'),
    path('categorias/', CategoryListView.as_view(), name='categorias'),


]