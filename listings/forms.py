from django import forms
from .models import Listing  # assuming Listing model exists in listings/models.py


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = '__all__' 
        
        
