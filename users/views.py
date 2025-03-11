from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, ExperienciaSerializer
from .models import ExperienciaModel

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Usuário criado com sucesso"},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ExperiencaListCreateView(generics.ListCreateAPIView):
    queryset = ExperienciaModel.objects.all()
    serializer_class = ExperienciaSerializer

class ExperienciaDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ExperienciaModel.objects.all()
    serializer_class = ExperienciaSerializer