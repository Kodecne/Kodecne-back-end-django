from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from users.models import User
from tecnologias.models import TecnologiaModel
from posts.models import PostModel
from users.serializers import PublicUserSerializer
from tecnologias.serializers import TecnologiaSerializer
from posts.serializers import PostSerializer

class SearchAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = request.query_params.get('query', '').strip()
        search_type = request.query_params.get('type', '').strip()

        if not query:
            return Response({"error": "O parâmetro 'query' é obrigatório."}, status=400)

        if search_type == 'user':
            users = User.objects.filter(Q(name__icontains=query) | Q(email__icontains=query))
            serializer = PublicUserSerializer(users, many=True, context={'request': request})
            return Response({"users": serializer.data})

        elif search_type == 'tecnologia':
            tecnologias = TecnologiaModel.objects.filter(nome__icontains=query)
            serializer = TecnologiaSerializer(tecnologias, many=True)
            return Response({"tecnologias": serializer.data})

        elif search_type == 'post':
            posts = PostModel.objects.filter(Q(texto__icontains=query) | Q(autor__name__icontains=query))
            serializer = PostSerializer(posts, many=True, context={'request': request})
            return Response({"posts": serializer.data})

        return Response({"error": "O parâmetro 'type' deve ser 'user', 'tecnologia' ou 'post'."}, status=400)