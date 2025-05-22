from rest_framework import serializers
from .models import ChatMessage
from users.serializers import UserSerializer

class ChatMessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)

    class Meta:
        model = ChatMessage
        fields = ['id', 'sender', 'receiver', 'content', 'timestamp', 'is_read']