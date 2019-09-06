from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import LoginView
from user.views.register import register as re
from user.forms.LoginForm import LoginForm as LF
from django.contrib.auth import views


from django.urls import path

urlpatterns = [
    path('register/', re, name="register"),
    path('login/', views.LoginView.as_view(template_name="login.html", authentication_form=LF), name="login"),
    path('logout/', LogoutView.as_view(template_name="logout.html"), name="logout")
]