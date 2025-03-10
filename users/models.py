from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("O email é obrigatório")
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=60)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    bio = models.TextField(null=True)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    endereco = models.CharField(max_length=200, null=True)
    portfolio = models.URLField(blank=True, null=True)
    escolaridade = models.CharField(max_length=100, null=True)
    genero = models.CharField(max_length=50, choices=[('Feminino', 'Feminino'), ('Masculino', 'Masculino'), ('Outro', 'Outro')], null=True)
    data_nascimento = models.DateTimeField(null=True)
    
    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    
    def __str__(self):
        return self.email