from django.shortcuts import render
from django.db.models import Q, Max, Count
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import models
from .models import ChatMessage
from .serializers import ChatMessageSerializer, ConversationSerializer
from users.models import User

class ChatMessageListCreate(generics.ListCreateAPIView):
    serializer_class = ChatMessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        other_user_id = self.request.query_params.get('user_id')
        if other_user_id:
            # Buscar mensagens
            messages = ChatMessage.objects.filter(
                Q(sender=self.request.user, receiver_id=other_user_id) |
                Q(sender_id=other_user_id, receiver=self.request.user)
            ).order_by('timestamp')
            
            # Marcar mensagens recebidas como lidas
            unread_messages = messages.filter(
                receiver=self.request.user,
                is_read=False
            )
            unread_messages.update(is_read=True)
            
            return messages
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

class ConversationList(generics.ListAPIView):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Encontrar todos os usuários com quem o usuário atual conversou
        conversations = []
        
        # Encontrar usuários únicos com quem houve conversa
        user_ids = ChatMessage.objects.filter(
            Q(sender=user) | Q(receiver=user)
        ).values_list(
            'sender', 'receiver'
        ).distinct()

        unique_users = set()
        for sender_id, receiver_id in user_ids:
            if sender_id != user.id:
                unique_users.add(sender_id)
            if receiver_id != user.id:
                unique_users.add(receiver_id)

        for other_user_id in unique_users:
            other_user = User.objects.get(id=other_user_id)
            
            # Última mensagem da conversa
            last_message = ChatMessage.objects.filter(
                Q(sender=user, receiver_id=other_user_id) |
                Q(sender_id=other_user_id, receiver=user)
            ).latest('timestamp')

            # Contagem de mensagens não lidas
            unread_count = ChatMessage.objects.filter(
                sender_id=other_user_id,
                receiver=user,
                is_read=False
            ).count()

            conversations.append({
                'user': other_user,
                'last_message': last_message,
                'unread_count': unread_count
            })

        return sorted(conversations, key=lambda x: x['last_message'].timestamp, reverse=True)

class MarkMessagesAsRead(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        sender_id = request.data.get('sender_id')
        if sender_id:
            # Marca todas as mensagens não lidas deste remetente como lidas
            unread_messages = ChatMessage.objects.filter(
                sender_id=sender_id,
                receiver=request.user,
                is_read=False
            )
            unread_messages.update(is_read=True)
            return Response({'status': 'messages marked as read'})
        return Response({'error': 'sender_id not provided'}, status=400)
