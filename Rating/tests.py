from django.test import TestCase
from django.contrib.auth.models import User
from Rating.models import UserProfile, Beertype, Brewery, Beer, Rating, Recommendation, BlogEntry, Phrase

class UserProfileTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.profile = UserProfile.objects.create(user=self.user, about='Test About')

    def test_profile_creation(self):
        self.assertEqual(UserProfile.objects.count(), 1)
        self.assertEqual(self.profile.about, 'Test About')

class BeertypeTestCase(TestCase):
    def setUp(self):
        self.beertype = Beertype.objects.create(name='Test Beer', brewing_type='Test Brewing', Color='Test Color', origin='Test Origin', description='Test Description')

    def test_beertype_creation(self):
        self.assertEqual(Beertype.objects.count(), 1)
        self.assertEqual(self.beertype.name, 'Test Beer')

class BreweryTestCase(TestCase):
    def setUp(self):
        self.brewery = Brewery.objects.create(name='Test Brewery', display_name='Test Display Name', location='Test Location', founded_year=2000, description='Test Description')

    def test_brewery_creation(self):
        self.assertEqual(Brewery.objects.count(), 1)
        self.assertEqual(self.brewery.name, 'Test Brewery')

class BeerTestCase(TestCase):
    def setUp(self):
        self.brewery = Brewery.objects.create(name='Test Brewery', display_name='Test Display Name', location='Test Location', founded_year=2000, description='Test Description')
        self.beertype = Beertype.objects.create(name='Test Beer', brewing_type='Test Brewing', Color='Test Color', origin='Test Origin', description='Test Description')
        self.beer = Beer.objects.create(brewery=self.brewery, name='Test Beer', display_name='Test Display Name', style=self.beertype, alcohol_content=5.0, original_gravity=1.0, recommended_serving_temperature=5, is_organic=False, clarity='Clear', yeast='Test Yeast', is_gluten_free=False, description='Test Description')

    def test_beer_creation(self):
        self.assertEqual(Beer.objects.count(), 1)
        self.assertEqual(self.beer.name, 'Test Beer')

class RatingTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.brewery = Brewery.objects.create(name='Test Brewery', display_name='Test Display Name', location='Test Location', founded_year=2000, description='Test Description')
        self.beertype = Beertype.objects.create(name='Test Beer', brewing_type='Test Brewing', Color='Test Color', origin='Test Origin', description='Test Description')
        self.beer = Beer.objects.create(brewery=self.brewery, name='Test Beer', display_name='Test Display Name', style=self.beertype, alcohol_content=5.0, original_gravity=1.0, recommended_serving_temperature=5, is_organic=False, clarity='Clear', yeast='Test Yeast', is_gluten_free=False, description='Test Description')
        self.rating = Rating.objects.create(beer=self.beer, user=self.user, Color=5, Entry=5, body=5, finish=5, carbonation=5, acidity=5, bitterness=5, drinkability=5, price=2, recommended=True)

    def test_rating_creation(self):
        self.assertEqual(Rating.objects.count(), 1)
        self.assertEqual(self.rating.beer.name, 'Test Beer')
        self.assertEqual(self.rating.user.username, 'testuser')

class RecommendationTestCase(TestCase):
    def setUp(self):
        self.brewery = Brewery.objects.create(name='Test Brewery', display_name='Test Display Name', location='Test Location', founded_year=2000, description='Test Description')
        self.beertype = Beertype.objects.create(name='Test Beer', brewing_type='Test Brewing', Color='Test Color', origin='Test Origin', description='Test Description')
        self.beer = Beer.objects.create(brewery=self.brewery, name='Test Beer', display_name='Test Display Name', style=self.beertype, alcohol_content=5.0, original_gravity=1.0, recommended_serving_temperature=5, is_organic=False, clarity='Clear', yeast='Test Yeast', is_gluten_free=False, description='Test Description')
        self.recommendation = Recommendation.objects.create(name='Test Recommendation', beer=self.beer)

    def test_recommendation_creation(self):
        self.assertEqual(Recommendation.objects.count(), 1)
        self.assertEqual(self.recommendation.name, 'Test Recommendation')
        self.assertEqual(self.recommendation.beer.name, 'Test Beer')

class BlogEntryTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.blog_entry = BlogEntry.objects.create(title='Test Title', content='Test Content', author=self.user)

    def test_blog_entry_creation(self):
        self.assertEqual(BlogEntry.objects.count(), 1)
        self.assertEqual(self.blog_entry.title, 'Test Title')
        self.assertEqual(self.blog_entry.author.username, 'testuser')

class PhraseTestCase(TestCase):
    def setUp(self):
        self.phrase = Phrase.objects.create(phrase='Test Phrase', intextphrase='Test InTextPhrase')

    def test_phrase_creation(self):
        self.assertEqual(Phrase.objects.count(), 1)
        self.assertEqual(self.phrase.phrase, 'Test Phrase')
        self.assertEqual(self.phrase.intextphrase, 'Test InTextPhrase')
