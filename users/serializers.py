from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import *

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['email', 'name', 'password']
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class SeguidoresSerializer(serializers.ModelSerializer):
    seguidor = UserSerializer()
    seguido = UserSerializer()
    class Meta:
        model = SeguidoresModel
        fields = ['id', 'seguidor', 'seguido']

class ExperienciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExperienciaModel
        fields = ['usuario', 'tecnologia', 'nivel']