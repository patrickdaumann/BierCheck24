from django.contrib import admin
from .models import Beer
from .models import Rating

admin.site.register(Rating)
admin.site.register(Beer)