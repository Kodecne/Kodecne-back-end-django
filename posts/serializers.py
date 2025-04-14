from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import *
from users.serializers import PublicUserSerializer

User = get_user_model


class PostMidiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = MidiaPost
        fields = '__all__'
    def get_arquivo(self, obj):
        request = self.context.get('request')
        if obj.arquivo:
            # Retorna a URL completa com base na request
            return request.build_absolute_uri(obj.arquivo.url)
        return None
    
    
class PostSerializer(serializers.ModelSerializer):
    autor = PublicUserSerializer(read_only=True)
    midias = PostMidiaSerializer(many=True, read_only=True)
    class Meta:
        model = PostModel
        fields = '__all__'

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikesModel
        fields = '__all__'