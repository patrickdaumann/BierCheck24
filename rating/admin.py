from django.contrib import admin
from .models import Brewery, Beer, Beertype, Rating


# Register your models here.
admin.site.register(Brewery)
admin.site.register(Beer)
admin.site.register(Beertype)
admin.site.register(Rating)