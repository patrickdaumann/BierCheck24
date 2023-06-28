from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.staticfiles import finders
from django.http import HttpResponse
from .models import Beer, Brewery, Beertype, Rating

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.generic.list import ListView
from .forms import RatingFormByID, BeerForm
from django.db.models import Avg, Count, Q

# Hier werden die Routen für die Endpoints (URLs) eingetragen


# Homepage
def home(request):
    return render(request, 'home.html')

# About Seite
def about(request):
    return render(request, template_name='about.html')

# Teste Seite
def test(request):
    beers = Beer.objects.all()
    context = {'beers': beers}
    return render(request, 'test.html', context)

# News Seite
def news(request):
    return render(request, template_name='news.html')

# Detail Ansicht für die verschiedenen Bier Arten
def beertype_detail(request, beertype_id):
    beertype = Beertype.objects.get(id=beertype_id)
    context = {'beertype': beertype}
    return render(request, 'beertype_detail.html', context)


# Detailansicht für die Biere (Bspw. Früh Kölsch)
def beer_detail(request, beer_id):
    beer = Beer.objects.get(id=beer_id)
    ratings = Rating.objects.filter(beer=beer)
    average_ratings = ratings.aggregate(
        Avg('color'), Avg('entry'), Avg('body'),
        Avg('finish'), Avg('carbonation'), Avg('acidity'),
        Avg('bitterness'), Avg('drinkability'), Avg('price')
    )
    beer.recommended_count = Rating.objects.filter(beer=beer, recommended=True).count()
    beer.ratings_count = Rating.objects.filter(beer=beer).count()

    if beer.ratings_count > 0:
        recommended_percentage = (beer.recommended_count / beer.ratings_count) * 100
    else:
        recommended_percentage = 0
     
    context = {
        'beer': beer,
        'average_ratings': average_ratings,
        'recommended_count': beer.recommended_count,
        'ratings_count': beer.ratings_count,
        'recommended_percentage': recommended_percentage
    }
    return render(request, 'beer_detail.html', context)


# Listenansicht für alle Biere
def beer_list(request):
    styles = Beertype.objects.all()
    breweries = Brewery.objects.all()

    # Get filter parameters from request GET parameters
    style_filter = request.GET.get('style')
    alcohol_content = request.GET.get('alcohol_content')
    brewery_filter = request.GET.get('brewery')

    beers = Beer.objects.all()

    if style_filter:
        beers = beers.filter(style=style_filter)

    if alcohol_content:
        if alcohol_content == 'lt4':
            beers = beers.filter(alcohol_content__lt=4.0)
        elif alcohol_content == '4-5':
            beers = beers.filter(alcohol_content__range=(4.0, 5.0))
        elif alcohol_content == 'gt5':
            beers = beers.filter(alcohol_content__gt=5.0)

    if brewery_filter:
        beers = beers.filter(brewery=brewery_filter)


    #context = {'beers': beers}
    return render(request, 'beer_list.html', {'beers': beers, 'styles': styles, 'breweries': breweries,'alcohol_content': alcohol_content})


# Listenansicht für alle Brauereien
def brewery_list(request):
    breweries = Brewery.objects.all()
    context = {'breweries': breweries}
    return render(request, 'brewery_list.html', context)


def brewery_detail(request, brewery_id):
    brewery = Brewery.objects.get(id=brewery_id)
    context = {'brewery': brewery}
    return render(request, 'brewery_detail.html', context)


# Detailansicht für eine einzelne Bewertung
def rating_detail(request, rating_id):
    # rating = get_object_or_404(Rating, pk=rating_id)
    rating = Rating.objects.get(id=rating_id)
    context = {'rating': rating}
    return render(request, 'rating_detail.html', context)


# Nutzer Registrierung
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


# Nutzerlogin
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Hier kann man zu einer anderen URL weiterleiten
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')


# Nutzerlogout
def logout_user(request):
    logout(request)
    return redirect('home')

# Seite zum hinzufügen von Bieren


def add_beer(request):
    if request.method == 'POST':
        form = BeerForm(request.POST)
        if form.is_valid():
            display_name = form.cleaned_data['display_name']
            if Beer.objects.filter(display_name=display_name).exists():
                messages.error(request, f'A beer with the name "{display_name}" already exists.')
            else:
                form.save()
                return redirect('add_success')  # Weiterleitung zur Erfolgsseite 
    else:
        form = BeerForm()
    
    form.fields.pop('name')
    form.fields.pop('ratings_count')
    form.fields.pop('recommended_count')


    context = {'form': form}
    return render(request, 'add_beer.html', context)



# Bewertungsseite auf der eine Bewertung erstellt werden kann

def rate_beer_by_id(request, beer_id):
    beer = Beer.objects.get(id=beer_id)
    user = request.user
    form = RatingFormByID()

    if request.method == 'POST':
        # Check if the user has already rated the beer
        if Rating.objects.filter(beer=beer, user=user).exists():
            messages.error(request, 'You have already rated this beer.')
            return redirect('rating_failed')
        else:
            form = RatingFormByID(request.POST)
            if form.is_valid():
                rating = form.save(commit=False)
                rating.user = user
                rating.beer = beer
                rating.save()

                messages.success(request, 'Beer rated successfully!')

                # Update beer ratings count and recommended count
                beer.ratings_count = Rating.objects.filter(beer=beer).count()
                beer.recommended_count = Rating.objects.filter(beer=beer, recommended=True).count()
                beer.save()

                return redirect('rating_success')

    return render(request, 'rate_beer_by_id.html', {'form': form, 'beer': beer, 'ratings_count': beer.ratings_count, 'recommended_count': beer.recommended_count})


# Anzeige einer Erfolgsmeldung nach dem erstellen einer Bewertung
def rating_success(request):
    return render(request=request, template_name='rating_success.html')

# Anzeige einer Erfolgsmeldung nach dem erstellen einer Bewertung
def rating_failed(request):
    return render(request=request, template_name='rating_failed.html')

# Anzeige einer Erfolgsmeldung nach dem Hinzufügen eines Bieres
def add_success(request):
    return render(request=request, template_name='add_success.html')



def search_beer(request):
    if request.method == 'GET':
        query = request.GET.get('q')
        if query:
            beers = Beer.objects.filter(Q(display_name__icontains=query))
            return render(request, 'beer_list.html', {'beers': beers})
    return redirect('beer_list')