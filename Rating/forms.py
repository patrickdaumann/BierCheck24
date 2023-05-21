from django import forms
from .models import Rating,Beer

class RatingFormByID(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['recommended', 'color', 'entry', 'body', 'finish', 'carbonation', 'acidity', 'bitterness', 'drinkability', 'price']



class BeerForm(forms.ModelForm):
    class Meta:
        model = Beer
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'required': False}),  # Set required attribute to False
        }