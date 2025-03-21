from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import *

User = get_user_model

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostModel
        fields = '__all__'


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikesModel
        fields = '__all__'