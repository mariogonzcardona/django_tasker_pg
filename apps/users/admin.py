from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from apps.users.models import User

# Registramos el modelo User en el admin, con los campos que queremos mostrar como Personal info, Permissions, Important dates, y con los campos que queremos que sean de solo lectura como readonly_fields, agregamos el campo rol y projects para que se puedan editar en el admin, y con el filter_horizontal agregamos los campos que queremos que sean de tipo many to many.
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # Campos que se mostraran en el admin
    list_display = ('id','username','first_name','last_name','email','is_active')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )