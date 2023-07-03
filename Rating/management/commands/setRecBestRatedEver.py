# python3 manage.py changebeerofmonth
from Rating.models import Beer, Recommendation, Rating


from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Setzt die Empfehlung BestRatedEver auf das am besten bewertete Bier aller zeiten'

    def handle(self, *args, **options):
        beers = Beer.objects.filter(approvalstatus=True).all()
        RecBestRatedEver = Recommendation.objects.filter(name="BestRatedEver").first()

        BestRatedBeer = None
        BestRatedBeerAvg = 0

        for beer in beers:
            
            #Set Average Rating Score for Beer to 0
            sumAvgRating = 0

            #Get all Ratings for specified beer
            ratings = Rating.objects.filter(beer=beer)

            #iterate Ratings and calculate average
            for rating in ratings:
                AvgRating = 0
                AvgRating += rating.Color
                AvgRating += rating.Entry
                AvgRating += rating.body
                AvgRating += rating.finish
                AvgRating += rating.carbonation
                AvgRating += rating.acidity
                AvgRating += rating.bitterness
                AvgRating += rating.drinkability

                #Calculate Average for Rating and add to Sum
                AvgRating =  AvgRating / 8
                sumAvgRating += AvgRating

            #Calculate Average RatingScore for Beer
            sumAvgRating /= len(ratings)

            self.stdout.write(f"Beer: {beer.name} - {sumAvgRating}")

            #If beer is best -> Set new best beer
            if (BestRatedBeer == None or BestRatedBeerAvg < sumAvgRating):
                BestRatedBeer = beer
                BestRatedBeerAvg = sumAvgRating

        #Set recommendation to best Rated Beer
        RecBestRatedEver.beer = BestRatedBeer
        RecBestRatedEver.save()
        self.stdout.write(f"Set BestRatedEver Recommendation to: {BestRatedBeer}")



            
        