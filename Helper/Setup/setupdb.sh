#!/bin/zsh

python3 manage.py runserver
python3 manage.py makemigrations Rating
python3 manage.py migrate --run-syncdb  
python3 manage.py loaddata Users.json --app Rating 
python3 manage.py loaddata 20230713_alldata.json --app Rating


## Nicht mehr notwendig:
#python3 manage.py loaddata Beertypes.json --app Rating
#python3 manage.py loaddata Breweries.json --app Rating
#python3 manage.py loaddata Beers.json --app Rating
#python3 manage.py loaddata Recommendations.json --app Rating
#python3 manage.py loaddata Ratings_gen.json --app Rating


echo "<<python3 manage.py createsuperuser>> nicht vergessen!"
echo "<<python3 manage.py runserver>> zum starten ausführen!"