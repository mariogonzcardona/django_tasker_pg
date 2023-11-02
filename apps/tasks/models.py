from django.db import models
from ..users.models import User

# Creacion del modelo Task
class Task(models.Model):
    title = models.CharField(max_length=50,verbose_name='Titulo')
    description = models.CharField(max_length=250,verbose_name='Descripcion')
    user = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name='Usuario')
    completed = models.BooleanField(default=False,verbose_name='Completado')
    date_to_finish = models.DateField(null=True, blank=True,verbose_name='Fecha de finalizacion')
    
    updated_at = models.DateTimeField(auto_now=True,verbose_name='Fecha de actualizacion')
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='Fecha de creacion')
    
    status= models.BooleanField(default=True,verbose_name='Estatus')

    # Metodo para mostrar el titulo de la tarea
    def __str__(self):
        return self.title + ' | ' + self.description
    
    # Nuevo método para devolver si es completada como una cadena
    def get_completed_display(self):
        return 'Completada' if self.completed else 'No completada'

    # Nuevo método para devolver el estado como una cadena
    def get_status_display(self):
        return 'Activo' if self.status else 'Inactivo'
    
    class Meta:
        db_table = 'TASKER_task'
        managed = True
        verbose_name = 'Tarea'
        verbose_name_plural = 'Tareas'
        ordering = ['id']
