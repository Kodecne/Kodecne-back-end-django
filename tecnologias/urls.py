from django.urls import path
from .views import TecnologiaListCreateView, TecnologiaDetailView

app_name='tecnologias'

urlpatterns = [
    path("", TecnologiaListCreateView.as_view(), name="Tecnologia-list-create"),
    path("<int:pk>/", TecnologiaDetailView.as_view(), name="Tecnologia-detail"),
]
