from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Beer, Brewery, Beertype, Rating

# Hier werden die Routen für die Endpoints (URLs) eingetragen
def home(request):
    return render(request, 'home.html')

def test(request):
    return render(request=request, template_name='test.html')

def beertype_detail(request, beertype_id):
    beertype = Beertype.objects.get(id=beertype_id)
    context = {'beertype': beertype}
    return render(request, 'beertype_detail.html', context)

def beer_detail(request, beer_id):
    beer = Beer.objects.get(id=beer_id)
    context = {'beer': beer}
    return render(request, 'beer_detail.html', context)

def brewery_detail(request, brewery_id):
    brewery = Brewery.objects.get(id=brewery_id)
    context = {'brewery': brewery}
    return render(request, 'brewery_detail.html', context)

def rating_detail(request, rating_id):
    #rating = get_object_or_404(Rating, pk=rating_id)
    rating = Rating.objects.get(id=rating_id)
    context = {'rating': rating}
    return render(request, 'rating_detail.html', context)