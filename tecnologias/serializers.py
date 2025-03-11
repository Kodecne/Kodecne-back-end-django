from rest_framework import serializers
from .models import TecnologiaModel

class TecnologiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TecnologiaModel
        fields = ['id', 'nome', 'imagem']