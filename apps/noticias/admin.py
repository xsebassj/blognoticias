
from django.contrib import admin
from apps.noticias.models import Category, Post, PostImage, Comment, Like

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['titulo']
    search_fields = ['titulo']

class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'titulo', 'category', 'autor', 'created_at', 'allow_comments']
    search_fields = ['id', 'titulo', 'contenido', 'autor__username']  # Corregido: autor__username
    list_filter = ['category', 'created_at', 'allow_comments']
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs  # Superusuarios ven todos los posts
        return qs.filter(autor=request.user)
    
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is not None:
            return obj.autor == request.user  
        return super().has_change_permission(request, obj)
    
    def has_delete_permission(self, request, obj=None):
        """Permite a los superusuarios eliminar cualquier post"""
        if request.user.is_superuser:
            return True
        if obj is not None:
            return obj.autor == request.user 
        return super().has_delete_permission(request, obj)

class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'post', 'autor']
    search_fields = ['id', 'contenido', 'autor__username'] 
    list_filter = ['created_at', 'post']
    
    def get_queryset(self, request):
       
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs  
        return qs.filter(autor=request.user)  
    
    def has_change_permission(self, request, obj=None):
        """Permite a los superusuarios editar cualquier comentario"""
        if request.user.is_superuser:
            return True
        if obj is not None:
            return obj.autor == request.user 
        return super().has_change_permission(request, obj)
    
    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is not None:
            return obj.autor == request.user  # Solo pueden eliminar sus propios comentarios
        return super().has_delete_permission(request, obj)

class LikeAdmin(admin.ModelAdmin):
    list_display = ['autor', 'fecha', 'noticia']
    search_fields = ['noticia__titulo', 'autor__username']  # Corregido
    list_filter = ['fecha']
    
    def get_queryset(self, request):
        """Permite a los superusuarios ver todos los likes"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(autor=request.user)
    
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is not None:
            return obj.autor == request.user
        return super().has_change_permission(request, obj)
    
    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is not None:
            return obj.autor == request.user
        return super().has_delete_permission(request, obj)

def activate_images(modeladmin, request, queryset):
    updated = queryset.update(active=True)
    modeladmin.message_user(
        request, f"{updated} imágenes fueron activadas correctamente."
    )
activate_images.short_description = "Activar imágenes seleccionadas"

def deactivate_images(modeladmin, request, queryset):
    updated = queryset.update(active=False)
    modeladmin.message_user(
        request, f"{updated} imágenes fueron desactivadas correctamente."
    )
deactivate_images.short_description = "Desactivar imágenes seleccionadas"

class PostImageAdmin(admin.ModelAdmin):
    list_display = ('post', 'image', 'active', 'created_at')
    search_fields = ('post__id', 'post__titulo', 'image')  # Corregido: post__titulo
    list_filter = ('active', 'created_at')
    actions = [activate_images, deactivate_images]

admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(PostImage, PostImageAdmin)