from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from apps.blog_auth.fuctions import *

from apps.blog_auth.models import User

# Register your models here.

class CustomUser(UserAdmin):

    fieldsets = UserAdmin.fieldsets + (
    (None, {'fields': [ 'avatar']}),
    )
    add_fieldsets = (
    (None, {
        'classes': ('wide',),
        'fields': [ 'avatar', 'email', 'password1', 'password2']
    }),
    )




    actions = [
        add_to_registered,
        add_to_collaborators,
        add_to_admins,
        remove_from_registered,
        remove_from_collaborators,
        remove_from_admins,
    ]
admin.site.register(User,CustomUser)
admin.site.site_header = "Panel Punto Tecnológico"
admin.site.site_title = "Administración"
admin.site.index_title = "Gestión de contenidos"