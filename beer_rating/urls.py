"""
URL configuration for beer_rating project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rating.views import home
from accounts.views import register, login, logout_view, my_login_view
from rating.views import add_beer, beer_list, BeerDetailView, RatingCreateView, RatingSuccessView
from brewery.views import brewery_detail




urlpatterns = [
   
    path('', home, name='home'),
    path('beers/', beer_list , name='beers'),
    path('beer_detail/', BeerDetailView.as_view() , name='beer_detail'),
    path('admin/', admin.site.urls),
    path('register/', register, name='register'),
    path('add/', add_beer, name='add_beer'),
    path('logout/', logout_view, name='logout'),
    path('accounts/login/', my_login_view, name='login'),
    path('<int:pk>/', BeerDetailView.as_view(), name='beer_detail'),
    path('rate/<int:pk>/', RatingCreateView.as_view(), name='rate_beer'),
    path('rating_success/', RatingSuccessView.as_view(), name='rating_success'),
    path('brewery/<int:pk>/', brewery_detail , name='brewery_detail'),
    
]
