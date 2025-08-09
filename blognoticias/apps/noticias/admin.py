from django.contrib import admin
from apps.noticias.models import Category,Post,PostImage,Comment,like


# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display =['titulo',]
    search_fields =['titulo',]


class PostAdmin(admin.ModelAdmin):
    list_display =['id','titulo','category', 'autor', 'created_at']
    search_fields =['id','titulo','contenido','autor_username']

class CommentAdmin(admin.ModelAdmin):
    list_display =['id','created_at','post','autor']
    search_fields =['id','contenido','autor_username',]

class LikeAdmin(admin.ModelAdmin):
    list_display =['autor','fecha']
    search_fields =['noticia',]


class PostImageAdmin(admin.ModelAdmin):
    list_display =['post','created_at']
    search_fields =['image',]

admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(like, LikeAdmin)
admin.site.register(PostImage, PostImageAdmin)