# python3 manage.py changebeerofmonth
from Rating.models import Beer, Recommendation


from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Setzt die Recommendation BeerOfMonth durch angabe den Namens'

    def add_arguments(self, parser):
        parser.add_argument('beername', type=str)

    def handle(self, *args, **options):
        beername = options['beername']

        beer = Beer.objects.filter(name = beername).first()

        beerofmonth = Recommendation.objects.filter(name="BeerOfMonth").first()
        beerofmonth.beer = beer
        beerofmonth.save()

        self.stdout.write(f"Set {beer.name} as {beerofmonth}")





