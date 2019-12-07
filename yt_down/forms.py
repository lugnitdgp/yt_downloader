from django import forms
from django.contrib.auth.models import User

class Userform(forms.ModelForm):
    password = forms.PasswordInput()
    class Meta:
        model = User
        fields = ['username','email','password']
