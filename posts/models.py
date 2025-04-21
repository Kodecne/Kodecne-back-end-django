from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
import os
from django.utils.timezone import now

User = get_user_model()

def midia_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    timestamp = now().strftime("%Y%m%d%H%M%S%f")  # AnoMêsDiaHoraMinSeg
    new_filename = f"{timestamp}.{ext}"
    return os.path.join("midias_posts", new_filename)
def validar_midia(arquivo):
    ext = os.path.splitext(arquivo.name)[1]
    valid_extensions = [".jpg", ".png", ".jpeg", ".mp4", ".mkv"]
    if ext.lower() not in valid_extensions:
        raise ValidationError(f"Formato de arquivo não suportado: {ext}. Use PNG, JPEG, ou JPG.")

class PostModel(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    texto = models.TextField(max_length=3000, null=False)
    data = models.DateTimeField(auto_now_add=True)

class MidiaPost(models.Model):
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE, related_name='midias')
    arquivo = models.FileField(upload_to=midia_upload_path, validators=[validar_midia])

class LikesModel(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts_que_curtiu')
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE, related_name='likes')
    data = models.DateTimeField(auto_now_add=True)

class ComentarioModel(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comentarios_em_posts')
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE, related_name='comentarios')
    texto = models.TextField(max_length=350)
    data = models.DateTimeField(auto_now_add=True)