from django import forms
from .models import Realtor,Property
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm



class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['title', 'description', 'price', 'address', 'image'] 

        
class RealtorForm(forms.ModelForm):
    class Meta:
        model = Realtor
        fields = ['name', 'photo', 'description', 'phone', 'email']
        


class RealtorLoginForm(forms.Form):
    username = forms.CharField(max_length=150 ,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'enter username'}) )
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'enter username'}))


class CustomAdminLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={'autofocus': True, 'placeholder': 'Enter your username'})
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'})
    )