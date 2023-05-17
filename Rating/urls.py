from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import beertype_detail, beer_detail, brewery_detail, rating_detail, rate_beer, rating_success, beer_list, about



urlpatterns = [
    path('', views.home, name='home'),
    
    path('register/', views.register, name='register'),
    #path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('login/', views.login_user, name='login'),
    path('test/', views.test, name='test'),
    path('beertype/<int:beertype_id>/', beertype_detail,  name='beertype_detail'),
    path('beer/<int:beer_id>/', beer_detail,  name='beer_detail'),
    path('brewery/<int:brewery_id>/', brewery_detail,  name='brewery_detail'),
    path('rating/<int:rating_id>/', rating_detail,  name='rating_detail'),
    path('rate', rate_beer, name="rate_beer"),
    path('rating_success', rating_success, name='rating_success'),
    path('about', about, name="about"),
    path('beer_list', beer_list, name='beer_list')
]