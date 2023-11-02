from rest_framework.serializers import ModelSerializer, Serializer

from apps.users.models import User

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']
        read_only_fields = ['id']
        
class ListarUserSerializer(ModelSerializer):
    class Meta(UserSerializer.Meta):
        read_only_fields = ['id']