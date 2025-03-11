from django.db import models
from django.core.exceptions import ValidationError
import os
# Create your models here.

def validar_tecnologia_imagem(arquivo):
    ext = os.path.splitext(arquivo.name)[1]
    valid_extensions = [".svg"]
    if ext.lower() not in valid_extensions:
        raise ValidationError(f"Formato de arquivo não suportado: {ext}. Use SVG.")

class TecnologiaModel(models.Model):
    nome = models.CharField(unique=True, max_length=100)
    imagem = models.FileField(upload_to='tecnologias/', validators=[validar_tecnologia_imagem], null=True, blank=True)
    
    def __str__(self):
        return self.nome