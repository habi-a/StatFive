from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import LoginView

from django.urls import path

urlpatterns = [
    path('login/', LoginView.as_view(template_name="login.html"), name="login"),
    path('logout/', LogoutView.as_view(template_name=""), name="logout")
]