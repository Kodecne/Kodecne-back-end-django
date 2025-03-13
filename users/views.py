from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .serializers import RegisterSerializer, ExperienciaSerializer, SeguidoresSerializer
from .models import ExperienciaModel, SeguidoresModel

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

class SeguidoresListCreateView(generics.ListCreateAPIView):
    queryset = SeguidoresModel.objects.all()
    serializer_class = SeguidoresSerializer
    def perform_create(self, serializer):
        seguidor = serializer.validated_data.get('seguidor')
        seguido = serializer.validated_data.get('seguido')

        if seguidor == seguido:
            raise ValidationError({"detail": "Você não pode seguir a si mesmo!"})

        serializer.save(seguidor=seguidor)
class SeguidoresDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SeguidoresModel.objects.all()
    serializer_class = SeguidoresSerializer

class ExperiencaListCreateView(generics.ListCreateAPIView):
    queryset = ExperienciaModel.objects.all()
    serializer_class = ExperienciaSerializer
class ExperienciaDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ExperienciaModel.objects.all()
    serializer_class = ExperienciaSerializer