from django.urls import path
from .views import ChatMessageListCreate, ChatMessageUnread

urlpatterns = [
    path('messages/', ChatMessageListCreate.as_view()),
    path('unread/', ChatMessageUnread.as_view()),
]
