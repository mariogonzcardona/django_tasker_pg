from rest_framework.permissions import BasePermission

# Mas adelante en el codigo, en el archivo views.py, se importa esta clase y se usa como parametro en la clase de la vista, que es la que se encarga de manejar las peticiones y respuestas de la API, con roles de usuario y permisos de acceso
class CustomPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False