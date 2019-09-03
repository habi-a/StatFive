from django import forms

class UploadForm(forms.Form):
    upload = forms.FileField()