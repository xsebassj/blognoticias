from django.contrib.auth.models import Group

def is_registered(self, obj):
    return obj.groups.filter(name='registered').exists()
is_registered.short_description = 'Es Usuario Registrado'
is_registered.boolean = True

def is_collaborator(self, obj):
    return obj.groups.filter(name='collaborators').exists()
is_collaborator.short_description = 'Es Colaborador'
is_collaborator.boolean = True

def is_admin(self, obj):
    return obj.groups.filter(name='admins').exists()
is_admin.short_description = 'Es Administrador'
is_admin.boolean = True

def add_to_registered(self, request, queryset):
    registered_group, created = Group.objects.get_or_create(name='registered')
    for user in queryset:
        user.groups.add(registered_group)
    self.message_user(
        request, "Los usuarios seleccionados fueron añadidos al grupo 'Registered'."
    )
add_to_registered.short_description = 'Agregar a Usuarios Registrados'

def add_to_collaborators(self, request, queryset):
    collaborators_group, created = Group.objects.get_or_create(name='collaborators')
    for user in queryset:
        user.groups.add(collaborators_group)
    self.message_user(
        request, "Los usuarios seleccionados fueron añadidos al grupo 'Collaborators'."
    )
add_to_collaborators.short_description = 'Agregar a Colaboradores'

def add_to_admins(self, request, queryset):
    admins_group, created = Group.objects.get_or_create(name='admins')
    for user in queryset:
        user.groups.add(admins_group)
    self.message_user(
        request, "Los usuarios seleccionados fueron añadidos al grupo 'Admins'."
    )
add_to_admins.short_description = 'Agregar a Administradores'

def remove_from_registered(self, request, queryset):
    try:
        registered_group = Group.objects.get(name='registered')
        for user in queryset:
            user.groups.remove(registered_group)
        self.message_user(
            request, "Los usuarios seleccionados fueron removidos del grupo 'Registered'."
        )
    except Group.DoesNotExist:
        self.message_user(
            request, "El grupo 'registered' no existe.", level='ERROR'
        )
remove_from_registered.short_description = 'Remover de Usuarios Registrados'

def remove_from_collaborators(self, request, queryset):
    try:
        collaborators_group = Group.objects.get(name='collaborators')
        for user in queryset:
            user.groups.remove(collaborators_group)
        self.message_user(
            request, "Los usuarios seleccionados fueron removidos del grupo 'Collaborators'."
        )
    except Group.DoesNotExist:
        self.message_user(
            request, "El grupo 'collaborators' no existe.", level='ERROR'
        )
remove_from_collaborators.short_description = 'Remover de Colaboradores'

def remove_from_admins(self, request, queryset):
    try:
        admins_group = Group.objects.get(name='admins')
        for user in queryset:
            user.groups.remove(admins_group)
        self.message_user(
            request, "Los usuarios seleccionados fueron removidos del grupo 'Admins'."
        )
    except Group.DoesNotExist:
        self.message_user(
            request, "El grupo 'admins' no existe.", level='ERROR'
        )
remove_from_admins.short_description = 'Remover de Administradores'
