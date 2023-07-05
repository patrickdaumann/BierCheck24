from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.staticfiles import finders
from django.http import HttpResponse
from .models import Beer, Brewery, Beertype, Rating, Recommendation, User

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.generic.list import ListView
from .forms import RatingFormByID, BeerForm
from django.db.models import Avg, Count, Q, F

# Hier werden die Routen für die Endpoints (URLs) eingetragen


# Homepage
def home(request):
    beer_of_month = Recommendation.objects.get(name="BeerOfMonth")
    new_arrival = Recommendation.objects.get(name="NewArrival")
    best_rated_ever = Recommendation.objects.get(name="BestRatedEver")
    
    # Access the associated beer
    beer_of_month = beer_of_month.beer
    new_arrival = new_arrival.beer
    best_rated_ever = best_rated_ever.beer
    
    # Create the context dictionary with the recommendation variable
    context = {
        'beer_of_month': beer_of_month,
        'new_arrival' : new_arrival,
        'best_rated_ever' : best_rated_ever,
    }
    
    return render(request, 'home.html', context)

# About Seite
def about(request):
    return render(request, template_name='about.html')

# beer_list_ext Seite
def beer_list_ext(request):
    beers = Beer.objects.annotate(
        Color__avg=Avg('rating__Color'),
        Entry__avg=Avg('rating__Entry'),
        body__avg=Avg('rating__body'),
        finish__avg=Avg('rating__finish'),
        carbonation__avg=Avg('rating__carbonation'),
        acidity__avg=Avg('rating__acidity'),
        bitterness__avg=Avg('rating__bitterness'),
        drinkability__avg=Avg('rating__drinkability'),
        price__avg=Avg('rating__price')
    )
    
    styles = Beertype.objects.all()
    breweries = Brewery.objects.all()

    # Get filter parameters from request GET parameters
    style_filter = request.GET.get('style')
    alcohol_content = request.GET.get('alcohol_content')
    brewery_filter = request.GET.get('brewery')

    

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
    
    
    context = {'beers': beers, 'styles': styles, 'breweries': breweries,'alcohol_content': alcohol_content}
    return render(request, 'beer_list_ext.html', context)

# News Seite
def news(request):
    return render(request, template_name='news.html')

# Detail Ansicht für die verschiedenen Bier Arten


def beer_detail(request, beer_id):
    beer = Beer.objects.get(id=beer_id)
    ratings = Rating.objects.filter(beer=beer)
    average_ratings = ratings.aggregate(
        Avg('Color'), Avg('Entry'), Avg('body'),
        Avg('finish'), Avg('carbonation'), Avg('acidity'),
        Avg('bitterness'), Avg('drinkability'), Avg('price')
    )
    beer.recommended_count = Rating.objects.filter(beer=beer, recommended=True).count()
    beer.ratings_count = Rating.objects.filter(beer=beer).count()

    if beer.ratings_count > 0:
        recommended_percentage = (beer.recommended_count / beer.ratings_count) * 100
    else:
        recommended_percentage = 0

    # Calculate the overall rating excluding the price rating
    overall_rating = (
        (average_ratings['Color__avg'] or 0) + (average_ratings['Entry__avg'] or 0) +
        (average_ratings['body__avg'] or 0) + (average_ratings['finish__avg'] or 0) +
        (average_ratings['carbonation__avg'] or 0) + (average_ratings['acidity__avg'] or 0) +
        (average_ratings['bitterness__avg'] or 0) + (average_ratings['drinkability__avg'] or 0)
    ) / 8

    context = {
        'beer': beer,
        'average_ratings': average_ratings,
        'recommended_count': beer.recommended_count,
        'ratings_count': beer.ratings_count,
        'recommended_percentage': recommended_percentage,
        'overall_rating': overall_rating,
        'all_beers': Beer.objects.exclude(id=beer_id),
    }
    return render(request, 'beer_detail.html', context)



# Seite zum Biervergleich

from django.db.models import Avg

def compare_beers(request, beer_id):
    if request.method == 'POST':
        # Retrieve the selected beer IDs
        beer1_id = beer_id
        beer2_id = request.POST.get('second_beer')

        # Get the beer objects
        beer1 = Beer.objects.get(id=beer1_id)
        beer2 = Beer.objects.get(id=beer2_id)

        # Get the ratings for both beers
        beer1_ratings = Rating.objects.filter(beer=beer1)
        beer2_ratings = Rating.objects.filter(beer=beer2)

        # Calculate the average ratings for both beers
        beer1_average_ratings = beer1_ratings.aggregate(
            Avg('Color'), Avg('Entry'), Avg('body'),
            Avg('finish'), Avg('carbonation'), Avg('acidity'),
            Avg('bitterness'), Avg('drinkability'), Avg('price')
        )
        beer2_average_ratings = beer2_ratings.aggregate(
            Avg('Color'), Avg('Entry'), Avg('body'),
            Avg('finish'), Avg('carbonation'), Avg('acidity'),
            Avg('bitterness'), Avg('drinkability'), Avg('price')
        )

        beer1_overall_rating = (
        (beer1_average_ratings['Color__avg'] or 0) + (beer1_average_ratings['Entry__avg'] or 0) + (beer1_average_ratings['body__avg'] or 0)
         + (beer1_average_ratings['finish__avg'] or 0) + (beer1_average_ratings['carbonation__avg'] or 0) + (beer1_average_ratings['acidity__avg'] or 0)
         + (beer1_average_ratings['bitterness__avg'] or 0) + (beer1_average_ratings['drinkability__avg'] or 0) / 8
        )

        beer2_overall_rating = (
        (beer2_average_ratings['Color__avg'] or 0) + (beer2_average_ratings['Entry__avg'] or 0) + (beer2_average_ratings['body__avg'] or 0)
         + (beer2_average_ratings['finish__avg'] or 0) + (beer2_average_ratings['carbonation__avg'] or 0) + (beer2_average_ratings['acidity__avg'] or 0)
         + (beer2_average_ratings['bitterness__avg'] or 0) + (beer2_average_ratings['drinkability__avg'] or 0) / 8
        )

        context = {
            'beer1': beer1,
            'beer2': beer2,
            'beer1_average_ratings': beer1_average_ratings,
            'beer2_average_ratings': beer2_average_ratings,
            'beer1_overall_rating': beer1_overall_rating,
            'beer2_overall_rating': beer2_overall_rating
        }
        return render(request, 'compare_beers.html', context)

    return redirect('beer_detail', beer_id=beer_id)





# Listenansicht für alle Biere
def beer_list(request):
    styles = Beertype.objects.all()
    breweries = Brewery.objects.all()

    # Get filter parameters from request GET parameters
    style_filter = request.GET.get('style')
    alcohol_content = request.GET.get('alcohol_content')
    brewery_filter = request.GET.get('brewery')

    beers = Beer.objects.filter(approvalstatus=True)

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

    beers = beers.order_by('display_name')  # Order beers by display name in ascending order
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
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            
           
            form.save()
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    
    return render(request, 'register.html', {'form': form})






# Nutzerlogin
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        # Clear any existing messages if not a POST request
        storage = messages.get_messages(request)
        storage.used = True
    
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
            beer = form.save(commit=False)
            beer.name = form.cleaned_data['display_name']
            if Beer.objects.filter(display_name=beer.name).exists():
                messages.error(request, f'A beer with the name "{beer.name}" already exists.')
            else:
                beer.save()
                return redirect('add_success')
    else:
        form = BeerForm()
    
    form.fields.pop('name')
    form.fields.pop('approvalstatus')
    form.fields.pop('ratings_count')
    form.fields.pop('recommended_count')

    context = {'form': form}
    return render(request, 'add_beer.html', context)



# Bewertungsseite auf der eine Bewertung erstellt werden kann


from django.contrib import messages

def rate_beer_by_id(request, beer_id):
    beer = Beer.objects.get(id=beer_id)
    user = request.user

    class CustomRatingFormByID(RatingFormByID):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            custom_labels = {
                'recommended': 'Empfohlen (0-10)',
                'Color': 'Farbe (0-10) ',
                'Entry': 'Einstieg (0-10)' ,
                'body': 'Körper (0-10)',
                'finish': 'Abgang (0-10)',
                'carbonation': 'Kohlensäure (0-10)',
                'acidity': 'Säure (0-10)',
                'bitterness': 'Bitterkeit (0-10)',
                'drinkability': 'Süffigkeit (0-10)',
                'price': 'Preis (1-3)'
                # Add custom labels for other fields here
            }
            for field_name, label in custom_labels.items():
                self.fields[field_name].label = label

    if request.method == 'POST':
        # Check if the user has already rated the beer
        if Rating.objects.filter(beer=beer, user=user).exists():
            messages.error(request, 'You have already rated this beer.', extra_tags='rating_error')
            return redirect('rating_failed')

        form = CustomRatingFormByID(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.user = user
            rating.beer = beer
            rating.save()

            messages.success(request, 'Beer rated successfully!', extra_tags='rating_success')

            # Update beer ratings count and recommended count
            beer.refresh_from_db()  # Refresh the beer object from the database
            beer.ratings_count = Rating.objects.filter(beer=beer).count()
            beer.recommended_count = Rating.objects.filter(beer=beer, recommended=True).count()
            beer.save()

            return redirect('rating_success')
        else:
            # Add form errors to the messages framework
            for field, errors in form.errors.items():
                for error in errors:
                    # Get the custom label for the field, if available
                    label = form.fields[field].label or field.capitalize()
                    messages.error(request, f'Error in {label}: {error}')
    else:
        form = CustomRatingFormByID()

    context = {
        'form': form,
        'beer': beer,
        'ratings_count': beer.ratings_count,
        'recommended_count': beer.recommended_count,
        'messages': messages.get_messages(request),  # Add messages to the context
    }

    return render(request, 'rate_beer_by_id.html', context)








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