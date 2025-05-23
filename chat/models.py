from django.db import models
from users.models import User
from django.utils.timezone import now

def chat_image_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    timestamp = now().strftime("%Y%m%d%H%M%S")
    return f'chat_images/{instance.sender.id}_{timestamp}.{ext}'

class ChatMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField(blank=True)
    images = models.JSONField(default=list, blank=True)  # Armazenará uma lista de URLs
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']
