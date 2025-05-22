from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import models
from .models import ChatMessage
from .serializers import ChatMessageSerializer

class ChatMessageListCreate(generics.ListCreateAPIView):
    serializer_class = ChatMessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        other_user_id = self.request.query_params.get('user_id')
        
        if other_user_id:
            return ChatMessage.objects.filter(
                (models.Q(sender=user) & models.Q(receiver_id=other_user_id)) |
                (models.Q(sender_id=other_user_id) & models.Q(receiver=user))
            ).order_by('timestamp')
        return ChatMessage.objects.none()

    def perform_create(self, serializer):
        receiver_id = self.request.data.get('receiver_id')
        serializer.save(sender=self.request.user, receiver_id=receiver_id)

class ChatMessageUnread(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        unread_count = ChatMessage.objects.filter(
            receiver=request.user,
            is_read=False
        ).count()
        return Response({'unread_count': unread_count})
