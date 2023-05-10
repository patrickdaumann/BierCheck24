from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from .models import Brewery

def brewery_detail(request, pk):
    brewery = get_object_or_404(Brewery, pk=pk)
    return render(request, 'brewery/brewery_detail.html', {'brewery': brewery})

