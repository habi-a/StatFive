from django import forms

class f(forms.Form):
    f = forms.FileField(widget=forms.ClearableFileInput())

class fs(forms.Form):
    fs = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
