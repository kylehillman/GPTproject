# forms.py
from django import forms

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(max_length=100, required=True, widget=forms.PasswordInput)