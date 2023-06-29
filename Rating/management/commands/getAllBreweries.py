# python3 manage.py changebeerofmonth
from Rating.models import Brewery


from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'gibt alle Brauereien mit Index fürs eintragen aus'

    def handle(self, *args, **options):
        breweries = Brewery.objects.all()

        for brewery in breweries:
            self.stdout.write(f"{brewery.pk} - {brewery.name}")





