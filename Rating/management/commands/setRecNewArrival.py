# python3 manage.py changebeerofmonth
from Rating.models import Beer, Recommendation


from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Setzt die Recommendation NewArrival auf das neueste freigegebene Bier (höchste ID)'

    def handle(self, *args, **options):
        
        new_arrival = Beer.objects.filter(approvalstatus=True).order_by('-id').first()

        beerofmonth = Recommendation.objects.filter(name="NewArrival").first()
        beerofmonth.beer = new_arrival
        beerofmonth.save()

        self.stdout.write(f"Set {new_arrival.name} as {beerofmonth}")





