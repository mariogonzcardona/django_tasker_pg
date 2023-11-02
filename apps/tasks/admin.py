from django.contrib import admin
from apps.tasks.models import Task

# Registramos el modelo de Task en el admin, con los campos que queremos mostrar.
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'user', 'completed', 'status', 'date_to_finish')
    list_filter = ('completed', 'status', 'updated_at', 'created_at')
    search_fields = ('title', 'description', 'user')
    ordering = ('id',)
