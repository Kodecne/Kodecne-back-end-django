from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
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

class CurtirPostAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        try:
            post = PostModel.objects.get(pk=post_id)
        except PostModel.DoesNotExist:
            return Response({"erro": "Post não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        like_existente = LikesModel.objects.filter(post=post, usuario=request.user).first()

        if like_existente:
            like_existente.delete()
            return Response({"mensagem": "Like removido com sucesso.", "likes":post.likes.count()}, status=status.HTTP_200_OK)
        else:
            LikesModel.objects.create(post=post, usuario=request.user)
            return Response({"mensagem": "Post curtido com sucesso.", "likes":post.likes.count()}, status=status.HTTP_201_CREATED)

class LikeListCreateView(generics.ListCreateAPIView):
    queryset = LikesModel.objects.all()
    serializer_class = LikeSerializer
class LikeDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = LikesModel.objects.all()
    serializer_class = LikeSerializer
    
class ComentarioListCreateView(generics.ListCreateAPIView):
    serializer_class = ComentarioSerializer

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return ComentarioModel.objects.filter(post_id=post_id).order_by('-data')

    def perform_create(self, serializer):
        post_id = self.kwargs['post_id']
        serializer.save(usuario=self.request.user, post_id=post_id)