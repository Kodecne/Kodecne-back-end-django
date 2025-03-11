from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("experiencias/", ExperiencaListCreateView.as_view(), name="Tecnologia-list-create"),
    path("experiencias/<int:pk>/", ExperienciaDetailsView.as_view(), name="Tecnologia-detail"),
]
