from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "nom d'utilisateur", 'required': 'true'}), label='')
    password = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type': "password", 'placeholder': "mot de passe"}),
        label='')

    class Meta:
        model = User
        fields = [
            'username',
            'password'
        ]

