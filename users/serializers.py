from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import ExperienciaModel, SeguidoresModel

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['email', 'name', 'password']
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class SeguidoresSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeguidoresModel
        fields = ['seguidor', 'seguido']

class ExperienciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExperienciaModel
        fields = ['usuario', 'tecnologia', 'nivel']