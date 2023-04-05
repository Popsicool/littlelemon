from django.urls import path
from . import views

urlpatterns = [
    path("", views.HelloAuthView, name="hello_auth"),
    path("signup", views.UserCreateView.as_view(), name="sign_up")
]