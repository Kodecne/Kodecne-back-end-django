from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import *
from users.serializers import PublicUserSerializer

User = get_user_model


class MidiaSerializer(serializers.ModelSerializer):
    tipo = serializers.SerializerMethodField()

    class Meta:
        model = MidiaPost
        fields = ['id', 'arquivo', 'tipo']

    def get_tipo(self, obj):
        if obj.arquivo.name.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
            return 'imagem'
        elif obj.arquivo.name.lower().endswith(('.mp4', '.mov', '.avi', '.mkv')):
            return 'video'
        return 'desconhecido'
    

class PostSerializer(serializers.ModelSerializer):
    autor = PublicUserSerializer(read_only=True)
    midias = MidiaSerializer(many=True, read_only=True)
    likes = serializers.SerializerMethodField()
    class Meta:
        model = PostModel
        fields = '__all__'
    
    def get_likes(self, obj):
        return obj.likes.count()

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikesModel
        fields = '__all__'