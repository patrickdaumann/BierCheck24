from django import forms
from .models import Beer, Rating, Brewery

class BeerForm(forms.ModelForm):
    brewery = forms.ModelChoiceField(queryset=Brewery.objects.all(), empty_label="Select brewery")
    class Meta:
        model = Beer
        fields = ('name', 'style', 'description', 'ibu', 'preis', 'brewery')
        

class RatingForm(forms.ModelForm):
    farbe = forms.IntegerField(widget=forms.NumberInput(attrs={'type': 'range', 'min': 0, 'max': 10, 'step': 1}), label='Farbe')
    einstieg = forms.IntegerField(widget=forms.NumberInput(attrs={'type': 'range', 'min': 0, 'max': 10, 'step': 1}), label='Einstieg')
    koerper = forms.IntegerField(widget=forms.NumberInput(attrs={'type': 'range', 'min': 0, 'max': 10, 'step': 1}), label='Körper')
    abgang = forms.IntegerField(widget=forms.NumberInput(attrs={'type': 'range', 'min': 0, 'max': 10, 'step': 1}), label='Abgang')
    kohlensaeure = forms.IntegerField(widget=forms.NumberInput(attrs={'type': 'range', 'min': 0, 'max': 10, 'step': 1}), label='Kohlensäure')
    bitterkeit = forms.IntegerField(widget=forms.NumberInput(attrs={'type': 'range', 'min': 0, 'max': 10, 'step': 1}), label='Bitterkeit')
    sueffigkeit = forms.IntegerField(widget=forms.NumberInput(attrs={'type': 'range', 'min': 0, 'max': 10, 'step': 1}), label='Süffigkeit')

    class Meta:
        model = Rating
        fields = ['farbe', 'einstieg', 'koerper', 'abgang', 'kohlensaeure', 'bitterkeit', 'sueffigkeit']
