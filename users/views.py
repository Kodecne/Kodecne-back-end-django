import random
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import LoginSerializer
from .serializers import *
from .models import *
from django.shortcuts import redirect
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
            user = serializer.save(is_active=False)

            verificacao = EmailVerification.objects.create(user=user)
            link = f"http://127.0.0.1:8000/users/email-verification?token={verificacao.token}"
            print(link)
            
            # send_mail(
            #     "Confirme seu email",
            #     f"Acesse: {link}",
            #     "kodecne@gmail.com",
            #     [user.email],
            #     fail_silently=False
            # )
            
            return Response(
                {"message": "Para confirmar que é você, verifique seu e-mail e insira o código enviado."},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmailVerificationView(APIView):
    def get(self,request):
        token = request.query_params.get('token')
        print(token)
        try:
            ver = EmailVerification.objects.get(token=token, is_used=False)
            ver.user.is_active = True
            ver.is_used = True
            ver.user.save()
            ver.save()
            return redirect('http://localhost:5173/login')
        except EmailVerification.DoesNotExist:
            return Response({"error": "Token inválido ou já utilizado"}, status=404)
            

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
    
    def patch(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True, context={"request": request})
        print(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

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
    