from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):

    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "nom d'utilisateur"}), label='')
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder': "prénom"}), label='')
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "nom"}), label='')
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "email"}), label='')
    password1 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'type': "password", 'placeholder': "mot de passe"}), label='')
    password2 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'type': "password", 'placeholder': "confirmation"}), label='')


    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        )


    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user