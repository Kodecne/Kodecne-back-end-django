from django.urls import path
from .views import *

urlpatterns = [
    path("", PostListCreateView.as_view(), name="post-list-create"),
    path('<int:pk>/', PostDetailsView.as_view(), name="post-details"),
    path('<int:post_id>/curtir/', CurtirPostAPIView.as_view(), name='curtir-post'),
    path('<int:post_id>/comentarios/', ComentarioListCreateView.as_view(), name='comentarios-post')
]
