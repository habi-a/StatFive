from django import forms

class c(forms.Form):
    c = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))

class t(forms.Form):
    t = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))
