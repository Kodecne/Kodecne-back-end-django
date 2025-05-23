from rest_framework import serializers
from django.conf import settings
from .models import ChatMessage
from users.serializers import UserSerializer
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.utils.timezone import now

class ChatMessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)
    images = serializers.ListField(
        child=serializers.FileField(max_length=1000000, allow_empty_file=False),
        write_only=True,
        required=False,
        default=list
    )

    class Meta:
        model = ChatMessage
        fields = ['id', 'content', 'images', 'sender', 'receiver', 'timestamp', 'is_read']
        read_only_fields = ['sender', 'timestamp', 'is_read']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # Converte os caminhos relativos em URLs completas apenas se houver imagens
        if instance.images:
            ret['images'] = [
                f"{settings.MEDIA_URL}{image_path}" for image_path in instance.images
            ]
        return ret

    def create(self, validated_data):
        try:
            # Extrai as imagens dos dados validados
            images = validated_data.pop('images', [])
            image_paths = []

            for image in images:
                if hasattr(image, 'read'):  # Verifica se é um objeto de arquivo válido
                    timestamp = now().strftime("%Y%m%d%H%M%S")
                    ext = image.name.split('.')[-1].lower()
                    
                    # Valida a extensão
                    if ext not in ['jpg', 'jpeg', 'png', 'gif']:
                        raise serializers.ValidationError(f"Formato de arquivo inválido: {ext}")
                    
                    # Gera um nome único para o arquivo
                    filename = f'chat_images/{validated_data["sender"].id}_{timestamp}.{ext}'
                    
                    # Salva o arquivo
                    content = ContentFile(image.read())
                    saved_path = default_storage.save(filename, content)
                    image_paths.append(saved_path)

            # Atualiza os dados validados com os caminhos das imagens
            validated_data['images'] = image_paths

            # Cria a mensagem
            return super().create(validated_data)
            
        except Exception as e:
            raise serializers.ValidationError(f"Erro ao processar imagens: {str(e)}")

class ConversationSerializer(serializers.Serializer):
    user = UserSerializer()
    last_message = ChatMessageSerializer()
    unread_count = serializers.IntegerField()