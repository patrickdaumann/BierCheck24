from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .views import beertype_detail, beer_detail, brewery_detail, rating_detail, rating_success, beer_list, about, test, brewery_list, rate_beer_by_id, news, add_beer
from .views import add_success, search_beer, rating_failed


urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_user, name='logout'),
    path('login/', views.login_user, name='login'),
    path('beertype/<int:beertype_id>/', beertype_detail,  name='beertype_detail'),
    path('beer/<int:beer_id>/', beer_detail,  name='beer_detail'),
    path('brewery/<int:brewery_id>/', brewery_detail,  name='brewery_detail'),
    path('rating/<int:rating_id>/', rating_detail,  name='rating_detail'),
    path('rating_success', rating_success, name='rating_success'),
    path('rating_failed', rating_failed, name='rating_failed'),
    path('about', about, name="about"),
    path('test', test, name="test"),
    path('news', news, name="news"),
    path('beer_list', beer_list, name='beer_list'),
    path('brewery_list', brewery_list, name='brewery_list'),
    path('ratebeerbyid/<int:beer_id>', rate_beer_by_id, name='rate_beer_by_id'),
    path('add_beer', add_beer, name='add_beer'),
    path('add_success', add_success, name='add_success'),
    path('search/', search_beer, name='search_beer')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
