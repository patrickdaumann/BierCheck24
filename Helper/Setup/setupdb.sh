#!/bin/zsh

python3 manage.py migrate --run-syncdb  
python3 manage.py loaddata Users.json --app Rating 
python3 manage.py loaddata Beertypes.json --app Rating
python3 manage.py loaddata Breweries.json --app Rating
python3 manage.py loaddata Beers.json --app Rating

echo "<<python3 manage.py createsuperuser>> nicht vergessen!"
echo "<<python3 manage.py runserver>> zum starten ausführen!"