from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from realtors.models import Realtor


# class CustomAdminLoginForm(AuthenticationForm):
#     username = forms.CharField(
#         label="Username",
#         widget=forms.TextInput(attrs={'autofocus': True, 'placeholder': 'Enter your username'})
#     )
#     password = forms.CharField(
#         label="Password",
#         widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'})
#     )

class CustomAdminLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={'autofocus': True, 'placeholder': 'Enter your username'})
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'})
    )
    

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class RealtorRegistrationForm(forms.ModelForm):
    class Meta:
        model = Realtor
        fields = ['name', 'photo', 'description', 'phone', 'email']