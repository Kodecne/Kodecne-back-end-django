from django.urls import path
from .views import ChatMessageListCreate, ConversationList, MarkMessagesAsRead

urlpatterns = [
    path('messages/', ChatMessageListCreate.as_view()),
    path('conversations/', ConversationList.as_view()),
    path('messages/read/', MarkMessagesAsRead.as_view()),
]
