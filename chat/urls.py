from django.urls import path
from .views import ChatMessageListCreate, ChatMessageUnread, ConversationList

urlpatterns = [
    path('messages/', ChatMessageListCreate.as_view()),
    path('conversations/', ConversationList.as_view()),
    path('unread/', ChatMessageUnread.as_view()),
]
