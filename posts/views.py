from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .serializers import *
from .models import *

User = get_user_model()
    
class PostListCreateView(generics.ListCreateAPIView):
    queryset = PostModel.objects.all().order_by('-data')
    serializer_class = PostSerializer
    
    def perform_create(self, serializer):
        serializer.save(autor=self.request.user)
    
class PostDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PostModel.objects.all()
    serializer_class = PostSerializer

class LikeListCreateView(generics.ListCreateAPIView):
    queryset = LikesModel.objects.all()
    serializer_class = LikeSerializer
class LikeDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = LikesModel.objects.all()
    serializer_class = LikeSerializer