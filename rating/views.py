from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from rating.models import Beer, Rating
from rating.forms import BeerForm, RatingForm
from django.template import RequestContext
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.db.models import Avg
from django.views.generic.edit import CreateView
from django.urls import reverse, reverse_lazy
from django.http import Http404
from django.contrib import messages
from django.views.generic.detail import DetailView
from django.views.generic import TemplateView
from django.utils import timezone



def home(request):
    context = {'user': request.user}
    print(request)
    return render(request, 'rating/home.html', context)


def beer_list(request):
    query = request.GET.get('q')
    filter = request.GET.get('filter')

    if query:
        beers = Beer.objects.filter(name__icontains=query)
    elif filter:
        beers = Beer.objects.filter(style=filter)
    else:
        beers = Beer.objects.all()

    return render(request, 'rating/beer_list.html', {'beers': beers})


class BeerDetailView(DetailView):
    model = Beer
    template_name = 'rating/beer_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        beer = self.object
        ratings = beer.ratings.all()
        if ratings:
            average_rating = Rating.objects.filter(beer=beer).aggregate(Avg('farbe'), Avg('einstieg'), Avg('koerper'), Avg('abgang'), Avg('kohlensaeure'), Avg('bitterkeit'), Avg('sueffigkeit'))
            context['average_rating'] = average_rating
        else:
            context['average_rating'] = 'No ratings yet'
        context['ratings'] = ratings  # add ratings to the context
        return context



def beer_list(request):
    user = request.user
    beers = Beer.objects.all()
    return render(request, 'rating/beer_list.html', {'beers': beers})

@login_required
def add_beer(request):
    user = request.user
    if request.method == 'POST':
        form = BeerForm(request.POST)
        if form.is_valid():
            beer = form.save(commit=False)
            beer.save()
            return redirect('beers')
    else:
        form = BeerForm()
    context = {'form': form, 'user': request.user}
    return render(request, 'rating/add_beer.html', {'form': form})


class RatingCreateView(LoginRequiredMixin, CreateView):
    template_name = 'rating/rate_beer.html'
    model = Rating
    fields = ['farbe', 'einstieg', 'koerper', 'abgang', 'kohlensaeure', 'bitterkeit', 'sueffigkeit']
    success_url = reverse_lazy('beer_list')

    def form_valid(self, form):
        rating = form.save(commit=False)
        beer_id = self.kwargs['pk']
        beer = get_object_or_404(Beer, id=beer_id)
        rating.beer = beer  # Set the beer object
        rating.user = self.request.user
        existing_rating = Rating.objects.filter(beer=beer, user=self.request.user).first()
        if existing_rating:
            messages.error(self.request, 'You have already rated this beer. Each user can only rate a beer once (for now)')
            
            return redirect('rate_beer', pk=beer_id)
        else:
            rating.farbe = form.cleaned_data['farbe']
            rating.einstieg = form.cleaned_data['einstieg']
            rating.koerper = form.cleaned_data['koerper']
            rating.abgang = form.cleaned_data['abgang']
            rating.kohlensaeure = form.cleaned_data['kohlensaeure']
            rating.bitterkeit = form.cleaned_data['bitterkeit']
            rating.sueffigkeit = form.cleaned_data['sueffigkeit']
            rating.save()
            
            return redirect(reverse('rating_success'))

class RatingSuccessView(TemplateView):
    template_name = 'rating/rating_success.html'