from django import forms
from .models import Rating

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['beer', 'color', 'entry', 'body', 'finish', 'carbonation', 'acidity', 'bitterness', 'drinkability', 'price']
