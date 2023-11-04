from rest_framework import serializers
from ..models import Task

# Serializer para Crear una nueva tarea.
class CrearTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id','title','description','date_to_finish']
        read_only_fields = ['id']

# Serializer para Listar todas las tareas.
class ListarTaskSerializer(serializers.ModelSerializer):
    # Obtenemos el email de user
    user=serializers.CharField(source='user.email')
    # completed = serializers.SerializerMethodField()
    # status = serializers.SerializerMethodField()
    
    # Formateamos la fecha de creacion y actualizacion.
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    
    class Meta:
        model = Task
        fields = ['id','title','description','user','completed','date_to_finish','updated_at','created_at','status']
        read_only_fields = ['id','updated_at','created_at','status']

    # Nuevo metodo para obtener si la tarea esta completada.
    def get_completed(self, obj):
        return obj.get_completed_display()
    
    # Nuevo metodo para obtener el estatus de la tarea.
    def get_status(self, obj):
        return obj.get_status_display()

# Serializer para Actualizar una tarea.
class ActualizarTaskSerializer(serializers.ModelSerializer):
    completed = serializers.BooleanField(default=False)
    
    class Meta:
        model = Task
        fields = ['title','description','completed','date_to_finish']

# Serializer para Eliminar una tarea de forma logica.
class DesactivarTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ()
        read_only_fields = ['id']