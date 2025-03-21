from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('', UserListCreateView.as_view(), name='users-list-create'),
    path('<int:pk>/', UserDetailsView.as_view(), name='users-detail'),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    path("experiencias/", ExperiencaListCreateView.as_view(), name="tecnologia-list-create"),
    path("experiencias/<int:pk>/", ExperienciaDetailsView.as_view(), name="tecnologia-detail"),

    path('seguidores/', SeguidoresListCreateView.as_view(), name='seguidores-list-create'),
    path('seguidores/<int:pk>/', SeguidoresDetailsView.as_view(), name='seguidores-detail')
]
