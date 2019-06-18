from django.urls import path
from Accounts.Enabled_Views.register import Register


urlpatterns = [
    path('register/', Register.as_view(), name='register'),
]