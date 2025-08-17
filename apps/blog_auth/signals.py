from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from apps.blog_auth.models import user
from django.dispatch import receiver
from django.db.models.signals import post_save
from apps.noticias.models import Post, Comment

@receiver(post_save, sender=user)
def create_groups_and_permissions(sender, instance, created, **kwargs):
    if created and instance.is_superuser:
        try:
            post_content_type = ContentType.objects.get_for_model(Post)
            comment_content_type = ContentType.objects.get_for_model(Comment)

            view_post_permission = Permission.objects.get(
                codename='view_post', content_type=post_content_type
            )
            add_post_permission = Permission.objects.get(
                codename='add_post', content_type=post_content_type
            )
            change_post_permission = Permission.objects.get(
                codename='change_post', content_type=post_content_type
            )
            delete_post_permission = Permission.objects.get(
                codename='delete_post', content_type=post_content_type
            )

            view_comment_permission = Permission.objects.get(
                codename='view_comment', content_type=comment_content_type
            )
            add_comment_permission = Permission.objects.get(
                codename='add_comment', content_type=comment_content_type
            )
            change_comment_permission = Permission.objects.get(
                codename='change_comment', content_type=comment_content_type
            )
            delete_comment_permission = Permission.objects.get(
                codename='delete_comment', content_type=comment_content_type
            )

            registered_group, created = Group.objects.get_or_create(name='registered')
            registered_group.permissions.add(
                view_post_permission, view_comment_permission,
                add_comment_permission, change_comment_permission,
                delete_comment_permission
            )

            collaborators_group, created = Group.objects.get_or_create(name='collaborators')
            collaborators_group.permissions.add(
                view_post_permission, add_post_permission,
                change_post_permission, delete_post_permission,
                view_comment_permission, add_comment_permission,
                change_comment_permission, delete_comment_permission
            )

            admins_group, created = Group.objects.get_or_create(name='admins')
            admins_group.permissions.add(
                view_post_permission, add_post_permission,
                change_post_permission, delete_post_permission,
                view_comment_permission, add_comment_permission,
                change_comment_permission, delete_comment_permission
            )

            print("Grupos y Permisos creados exitosamente.")

        except ContentType.DoesNotExist:
            print("El tipo aun no se encuentra disponible.")
        except Permission.DoesNotExist:
            print("Uno o mas permisos no se encuentran disponibles")






