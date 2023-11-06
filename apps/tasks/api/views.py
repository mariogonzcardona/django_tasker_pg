from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from datetime import datetime
from django.utils import timezone
from util_common.pagination import CustomPagination
from apps.tasks.tasks import send_notification_email

# Generamos la Vista para el modelo Task.
class TaskViewSet(ModelViewSet):
    queryset = Task.objects.filter(status=True)
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    # filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    
    # search_fields = ['clave', 'nombre', 'siglas']
    # ordering_fields = ['clave', 'nombre', 'siglas']
    # ordering = ['clave', 'nombre', 'siglas']
    
    # Metodos permitidos para el endpoint de Task.
    http_method_names = ['get', 'post', 'put', 'delete']
    
    # Se agregan los serializers para cada accion
    serializer_class = {
        'list': ListarTaskSerializer,
        'retrieve': ListarTaskSerializer,
        'create': CrearTaskSerializer,
        'destroy': DesactivarTaskSerializer,
        'update': ActualizarTaskSerializer,
    }
    
    # Se establece el serializer para cada accion
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ListarTaskSerializer
        elif self.action in ['create']:
            return CrearTaskSerializer
        elif self.action in ['update']:
            return ActualizarTaskSerializer
        elif self.action in ['destroy']:
            return DesactivarTaskSerializer
        
    # Sobre escribimos el metodo crear una tarea.
    def create(self, request, *args, **kwargs):
        try:
            # Obtenemso el usuario logueado.
            user = request.user
            
            # Validamos que la fecha de finalizacion no sea menor a la fecha de creacion.
            date_to_finish = datetime.strptime(request.data['date_to_finish'], '%Y-%m-%d').date()
            if date_to_finish < datetime.now().date():
                return Response({'detail':'La fecha de finalizacion no puede ser menor a la fecha de creacion.'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Usamos el serializer para crear la tarea.
            serializer = CrearTaskSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=user)
            
            # Enviamos correo de notificacion, de creacion de tarea.
            context = {
                'request':request,
                'action_type':'crear_tarea',
                'user_email':user.email,
                'full_name':f'{user.first_name} {user.last_name}',
            }
            send_notification_email(**context)
            
            # Retornamos la respuesta.
            return Response({'detail':'Tarea creada.'}, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({'detail':str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    # Sobre escribimos el método actualizar una tarea.
    def update(self, request, *args, **kwargs):
        try:
            # Obtenemos el usuario logueado.
            user = request.user
            
            # Obtenemos el objeto a actualizar.
            instance = self.get_object()

            # Obtenemos el estado 'completed' desde los datos de la petición
            completed_in_request = request.data.get('completed', False)

            # Validamos si la tarea ya estaba completada antes.
            if instance.completed:
                # Si la tarea está completada, no se puede actualizar.
                return Response({'detail':'No se puede actualizar una tarea completada.'}, status=status.HTTP_400_BAD_REQUEST)

            # Si la tarea no está completada, se actualiza, y se retorna la respuesta con un mensaje.
            else:
                # Se actualiza la tarea.
                instance.title = request.data['title']
                instance.description = request.data['description']

                # Convertimos la fecha de finalización enviada desde el frontend a un objeto datetime
                date_to_finish = datetime.strptime(request.data['date_to_finish'], '%Y-%m-%d').date()

                # Nos aseguramos que la fecha date_to_finish no pueda ser menor a la fecha de creacion.
                if date_to_finish < instance.created_at.date():
                    return Response({'detail': 'La fecha de finalización no puede ser menor a la fecha de creación.'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    instance.date_to_finish = date_to_finish

                # Si se marca la tarea como completada y no estaba completada previamente, actualizamos la fecha de finalización.
                if completed_in_request and not instance.completed:
                    instance.date_to_finish = timezone.now().date()

                # Actualizamos el estado 'completed' según los datos de la petición.
                instance.completed = completed_in_request

                instance.save()
                
                # Enviamos correo de notificación, de actualización de tarea.
                context = {
                    'request': request,
                    'action_type': 'actualizacion_tarea',
                    'user_email': user.email,
                    'full_name': f'{user.first_name} {user.last_name}',
                }
                send_notification_email(**context)
                
                # Se retorna la respuesta.
                return Response({'detail':'Tarea actualizada.'}, status=status.HTTP_200_OK)
                
        except Exception as e:
            return Response({'detail':str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    # Sobre escribimos el metodo eliminar una tarea, ya que no se elimina, solo se desactiva.
    def destroy(self, request, *args, **kwargs):
       try:
        # Obtenemos el usuario logueado.
        user = request.user
        
        # Obtenemos el objeto a eliminar.
        instance = self.get_object()
        # Validamos si la tarea esta completada.
        if instance.completed:
            # Si la tarea esta completada, no se puede eliminar.
            return Response({'detail':'No se puede eliminar una tarea completada.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Si la tarea no esta completada, se elimina, y se retorna la respuesta con un mensaje.
        else:
            # Se elimina la tarea.
            instance = self.get_object()
            instance.status = False
            instance.save()
            
            # Enviamos correo de notificacion, de actualizacion de tarea.
            context = {
                'request':request,
                'action_type':'eliminacion_tarea',
                'user_email':user.email,
                'full_name':f'{user.first_name} {user.last_name}',
            }
            send_notification_email(**context)
            # Se retorna la respuesta.
            return Response({'detail':'Tarea eliminada.'}, status=status.HTTP_200_OK)
       except Exception as e:
            return Response({'detail':str(e)}, status=status.HTTP_400_BAD_REQUEST)
    