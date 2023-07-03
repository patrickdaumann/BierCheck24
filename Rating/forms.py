from django import forms
from .models import Rating,Beer

class RatingFormByID(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['recommended', 'Farbe', 'Einstieg', 'body', 'finish', 'carbonation', 'acidity', 'bitterness', 'drinkability', 'price']



class BeerForm(forms.ModelForm):
    class Meta:
        model = Beer
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'required': False}),  # Attribute die nicht bei einem Bier benötigt werden
            'ratings_count': forms.TextInput(attrs={'required': False}),  
            'recommenden_count': forms.TextInput(attrs={'required': False}),  
        }