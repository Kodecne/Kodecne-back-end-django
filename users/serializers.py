from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import *

User = get_user_model()

class LoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['name'] = user.name
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = {
            'id': self.user.id,
            'email': self.user.email,
            'name': self.user.name,
        }
        return data

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        extra_kwargs = {"password": {"write_only": True}}
        fields = ['email', 'name', 'password']
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
class UserSerializer(serializers.ModelSerializer):
    github = serializers.URLField()
    linkedin = serializers.URLField()
    class Meta:
        model = User
        fields = '__all__'
    def get_imagem(self, obj):
        request = self.context.get('request')
        if obj.imagem:
            # Retorna a URL completa com base na request
            return request.build_absolute_uri(obj.imagem.url)
        return None

class PublicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'bio', 'escolaridade', 'imagem']
    def get_imagem(self, obj):
        request = self.context.get('request')
        if obj.imagem:
            # Retorna a URL completa com base na request
            return request.build_absolute_uri(obj.imagem.url)
        return None
    
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