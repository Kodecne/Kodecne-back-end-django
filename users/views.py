from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import LoginSerializer
from .serializers import *
from .models import *
from .permissions import IsAuthenticatedAndActive

User = get_user_model()

class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

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

# class LoginView(APIView):
#     def post(self, request):
#         email = request.data.get("email")
#         password = request.data.get("password")

#         user = authenticate(username=email, password=password)
#         if user is None:
#             return Response({"error": "Credenciais inválidas"}, status=status.HTTP_400_BAD_REQUEST)

#         refresh = RefreshToken.for_user(user)
#         return Response({
#             "access": str(refresh.access_token),
#             "refresh": str(refresh),
#         })

class UsersListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedAndActive]
    def get(self, request):
        serializer = UserSerializer(request.user, context={'request': request})
        return Response(serializer.data)

class UserDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedAndActive]
    def get(self, request):
        serializer = UserSerializer(request.user, context={'request': request})
        return Response(serializer.data)

class MeView(APIView):
    permission_classes = [IsAuthenticatedAndActive]

    def get(self, request):
        serializer = UserSerializer(request.user, context={'request': request})
        return Response(serializer.data)

class SeguidoresListCreateView(generics.ListCreateAPIView):
    queryset = SeguidoresModel.objects.all()
    serializer_class = SeguidoresSerializer
    permission_classes = [IsAuthenticatedAndActive]
    def perform_create(self, serializer):
        seguidor = serializer.validated_data.get('seguidor')
        seguido = serializer.validated_data.get('seguido')

        if seguidor == seguido:
            raise ValidationError({"detail": "Você não pode seguir a si mesmo!"})

        serializer.save(seguidor=seguidor)
class SeguidoresDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SeguidoresModel.objects.all()
    serializer_class = SeguidoresSerializer
    permission_classes = [IsAuthenticatedAndActive]

class ExperiencaListCreateView(generics.ListCreateAPIView):
    queryset = ExperienciaModel.objects.all()
    serializer_class = ExperienciaSerializer
    permission_classes = [IsAuthenticatedAndActive]

class ExperienciaDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ExperienciaModel.objects.all()
    serializer_class = ExperienciaSerializer
    permission_classes = [IsAuthenticatedAndActive]
    