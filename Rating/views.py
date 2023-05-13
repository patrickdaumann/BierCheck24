from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Beer, Brewery, Beertype, Rating

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .forms import RatingForm

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

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)

            # Redirect nach erfolgreicher anmeldung
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home') # Hier kann man zu einer anderen URL weiterleiten
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('home')


def rate_beer(request):
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.user = request.user
            rating.save()
            return redirect('rating_success') # Weiterleitung zur Erfolgsseite
    else:
        form = RatingForm()
    return render(request, 'rate_beer.html', {'form': form})

def rating_success(request):
    return render(request=request, template_name='rating_success.html')