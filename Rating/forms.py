from django import forms
from .models import Rating

class RatingFormByID(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['recommended', 'color', 'entry', 'body', 'finish', 'carbonation', 'acidity', 'bitterness', 'drinkability', 'price']
