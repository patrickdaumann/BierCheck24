from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone







class Beer(models.Model):
    name = models.CharField(max_length=255)
    style = models.CharField(max_length=255)
    ibu = models.FloatField()
    description = models.TextField()
    preis = models.FloatField(default = 0)
    brewery = models.ForeignKey('brewery.Brewery', on_delete=models.SET_NULL, null=True, blank=True)

    def get_absolute_url(self):
        return reverse('beer_detail', args=[str(self.id)])
    
    

   

    
class Rating(models.Model):
    beer = models.ForeignKey(Beer, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default= timezone.now, blank=True)
    farbe = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)])
    einstieg = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)])
    koerper = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)])
    abgang = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)])
    kohlensaeure = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)])
    bitterkeit = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)])
    sueffigkeit = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)])



class Brewery(models.Model):
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name