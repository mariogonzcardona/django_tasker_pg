from apps.users.api.serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
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
        # No hay necesidad de buscar ni eliminar tokens de la base de datos,
        # simplemente se devuelve una respuesta de éxito
        return Response({'detail': 'Logout successful'}, status=status.HTTP_200_OK)

class VerifyTokenView(APIView):
    def post(self, request):
        token = request.data.get('token')

        if not token:
            return Response({'detail': 'No se proporcionó token'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Intenta validar el token
            access_token = AccessToken(token)
            access_token.check_exp()

            # Puedes obtener el usuario del token si es necesario
            user = User.objects.get(id=access_token['user_id'])
            print(user)

            return Response({'detail': 'Token válido', 'token': str(access_token)}, status=status.HTTP_200_OK)
        except TokenError as e:
            # Si el token es inválido o ha expirado
            return Response({'detail': 'Token inválido', 'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
