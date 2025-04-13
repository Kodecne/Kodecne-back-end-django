from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import *
from users.serializers import PublicUserSerializer

User = get_user_model

class PostSerializer(serializers.ModelSerializer):
    autor = PublicUserSerializer(read_only=True)
    class Meta:
        model = PostModel
        fields = '__all__'

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikesModel
        fields = '__all__'