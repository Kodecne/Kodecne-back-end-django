from django.urls import path
from .views import *

urlpatterns = [
    path("", PostListCreateView.as_view(), name="post-list-create"),
]
