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
    
class ComentarioSerializer(serializers.ModelSerializer):
    usuario = PublicUserSerializer(read_only=True)
    class Meta:
        model = ComentarioModel
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    autor = PublicUserSerializer(read_only=True)
    midias = MidiaSerializer(many=True, read_only=True)
    curtidas = serializers.SerializerMethodField()
    curtido_por_mim = serializers.SerializerMethodField()  # 🚀 campo extra
    comentarios = ComentarioSerializer(many=True, read_only=True)

    class Meta:
        model = PostModel
        fields = '__all__'

    def get_curtidas(self, obj):
        return obj.likes.count()

    def get_curtido_por_mim(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return LikesModel.objects.filter(post=obj, usuario=user).exists()
    
class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikesModel
        fields = '__all__'

