from django import forms
from django.contrib.auth.models import User

class loginForm(forms.ModelForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput())
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
         model = User
         fields = ['email', 'password']