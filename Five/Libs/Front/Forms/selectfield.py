from django import forms

class s(forms.Form):
    s = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control '}))

class sm(forms.Form):
    sm = forms.MultipleChoiceField(
        widget=forms.SelectMultiple(attrs={'class':'form-control '})
        )
