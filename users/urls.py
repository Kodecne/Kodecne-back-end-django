from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    # path("", UsersListCreateView.as_view(), name="user-list-create"),
    # path("<int:pk>/", UserDetailsView.as_view(), name="user-detail"),
    path("me/", MeView.as_view(), name='me'),
    path('email-verification/', EmailVerificationView.as_view(), name='email-verification'),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("experiencias/", ExperiencaListCreateView.as_view(), name="experiencias-list-create"),
    path("experiencias/<int:pk>/", ExperienciaDetailsView.as_view(), name="experiencias-detail"),
    path('seguidores/', SeguidoresListCreateView.as_view(), name='seguidores-list-create'),
    path('seguidores/<int:pk>/', SeguidoresDetailsView.as_view(), name='seguidores-detail')
]
