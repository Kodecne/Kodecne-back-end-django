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
        post = serializer.save(autor=self.request.user)
        
        midias = self.request.FILES.getlist('midias')
        for midia in midias:
            MidiaPost.objects.create(post=post, arquivo=midia)
    
    def get_queryset(self):
        user = self.request.user  # Pega o usuário autenticado
        user_id = self.request.query_params.get('user_id')  # Pega o ID do usuário da URL
        
        print(user_id)
        if user_id:
            return PostModel.objects.filter(autor_id=user_id).order_by('-data')
        return PostModel.objects.all().order_by('-data')
    
class PostDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PostModel.objects.all()
    serializer_class = PostSerializer

class LikeListCreateView(generics.ListCreateAPIView):
    queryset = LikesModel.objects.all()
    serializer_class = LikeSerializer
class LikeDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = LikesModel.objects.all()
    serializer_class = LikeSerializer