from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models
from django.core.exceptions import ValidationError
from tecnologias.models import TecnologiaModel
import os, uuid
from django.utils.timezone import now

def user_pic_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    timestamp = now().strftime("%Y%m%d%H%M%S%f")  # AnoMêsDiaHoraMinSeg
    new_filename = f"{timestamp}.{ext}"
    return os.path.join("user_pics", new_filename)

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

def validar_imagem_usuario(arquivo):
    ext = os.path.splitext(arquivo.name)[1]
    valid_extensions = [".jpg", ".png", ".jpeg"]
    if ext.lower() not in valid_extensions:
        raise ValidationError(f"Formato de arquivo não suportado: {ext}. Use PNG, JPEG, ou JPG.")

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=60, unique=True)
    imagem = models.FileField(upload_to=user_pic_upload_path, default='user_pics/default.png', validators=[validar_imagem_usuario], null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    bio = models.TextField(null=True)
    telefone = models.CharField(max_length=15, blank=True, null=True, unique=True)
    localidade = models.CharField(max_length=200, null=True)
    escolaridade = models.CharField(max_length=100, null=True)
    genero = models.CharField(max_length=50, choices=[('Feminino', 'Feminino'), ('Masculino', 'Masculino'), ('Outro', 'Outro')], null=True)
    linkedin = models.CharField(max_length=100, null=True)
    github = models.CharField(max_length=100, null=True)
    data_nascimento = models.DateTimeField(null=True)
    
    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    
    def __str__(self):
        return self.email

class SeguidoresModel(models.Model):
    seguidor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seguindo')
    seguido = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seguidores')

class ExperienciaModel(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='experiencias')
    tecnologia = models.ForeignKey(TecnologiaModel, on_delete=models.CASCADE)
    nivel = models.CharField(max_length=20, choices=[
        ('beginner', 'Iniciante'),
        ('intermediate', 'Intermediário'),
        ('advanced', 'Avançado'),
        ('expert', 'Expert')
    ])
    

class EmailVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='email_verification')
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)