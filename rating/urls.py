from django.urls import path
from . import views
from .views import beertype_detail, beer_detail, brewery_detail, rating_detail


urlpatterns = [
    path('', views.home, name='home'),
    path('test/', views.test, name='test'),
    path('beertype/<int:beertype_id>/', beertype_detail,  name='beertype_detail'),
    path('beer/<int:beer_id>/', beer_detail,  name='beer_detail'),
    path('brewery/<int:brewery_id>/', brewery_detail,  name='brewery_detail'),
    path('rating/<int:rating_id>/', rating_detail,  name='rating_detail'),
]