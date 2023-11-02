from apps.users.api.serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .serializers import *


# Funcion de Login con JWT
class LoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.user
            context={
                'full_name': f'{user.first_name} {user.last_name}',
                'access': response.data['access'],
                'refresh': response.data['refresh'],
            }
            return Response(context, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': 'Error al iniciar sesión, verifique sus credenciales'}, status=status.HTTP_400_BAD_REQUEST)

# Funcion de Logout con JWT
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Obtiene el token del usuario autenticado
        token = Token.objects.get(user=request.user)
        # Elimina el token
        token.delete()
        return Response({'detail': 'Logout successful'})
