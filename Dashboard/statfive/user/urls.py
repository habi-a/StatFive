from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import LoginView
from user.views.register import register as re

from django.urls import path

urlpatterns = [
    path('register/', re, name="register"),
    path('login/', LoginView.as_view(template_name="login.html"), name="login"),
    path('logout/', LogoutView.as_view(template_name="logout.html"), name="logout")
]