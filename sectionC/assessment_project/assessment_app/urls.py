from django.urls import path
from . import views

urlpatterns = [
    path("signup", views.Signup.as_view()),
    path("login", views.Login.as_view()),
    path("post", views.Post.as_view()),
]
