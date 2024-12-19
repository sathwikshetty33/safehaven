from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import *

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email','username', 'password1', 'password2']


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password1',]

class NgoRegisterForm(forms.ModelForm):
    class Meta:
        model = ngo
        fields = ['username', 'number', 'email', 'latitude', 'longitude']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'}),
            'number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
            'latitude': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter latitude'}),
            'longitude': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter longitude'}),
        }
