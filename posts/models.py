from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class PostModel(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    texto = models.TextField(max_length=3000, null=False)
    data = models.DateTimeField(auto_now_add=True)

class LikesModel(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts_que_curtiu')
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE, related_name='likes')
    data = models.DateTimeField(auto_now_add=True)