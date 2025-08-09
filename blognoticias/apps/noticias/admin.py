from django.contrib import admin
from apps.noticias.models import Category,Post,PostImage,Comment,like


# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display =['titulo',]
    search_fields =['titulo',]


class PostAdmin(admin.ModelAdmin):
    list_display =['id','titulo','category', 'autor', 'created_at','allow_comments']
    search_fields =['id','titulo','contenido','autor_username']

class CommentAdmin(admin.ModelAdmin):
    list_display =['id','created_at','post','autor']
    search_fields =['id','contenido','autor_username',]

class LikeAdmin(admin.ModelAdmin):
    list_display =['autor','fecha']
    search_fields =['noticia',]


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
    search_fields = ('post__id', 'post__title', 'image')
    list_filter = ('active', )

    actions = [activate_images, deactivate_images]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(like, LikeAdmin)
admin.site.register(PostImage, PostImageAdmin)