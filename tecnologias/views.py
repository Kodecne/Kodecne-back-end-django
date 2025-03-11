from rest_framework import generics
from .models import TecnologiaModel
from .serializers import TecnologiaSerializer

class TecnologiaListCreateView(generics.ListCreateAPIView):
    queryset = TecnologiaModel.objects.all()
    serializer_class = TecnologiaSerializer

class TecnologiaDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TecnologiaModel.objects.all()
    serializer_class = TecnologiaSerializer
