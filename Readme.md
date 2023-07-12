# Install

```bash
git clone git@github.com:patrickdaumann/BierCheck24.git

cd BierCheck24

python3 manage.py migrate --run-syncdb

python3 manage.py createsuperuser

python3 manage.py loaddata Beertypes.json --app Rating
python3 manage.py loaddata Breweries.json --app Rating
python3 manage.py loaddata Beers.json --app Rating
python3 manage.py loaddata Recommendations.json --app Rating
python3 manage.py loaddata news_entries.json --app Rating     Wichtig: Funktioniert nur, wenn die User importiert wurden, ansonsten bitte news_entries+users.json!

pip install django-bootstrap-v5
pip install pillow

python3 manage.py runserver



```

- Nach einem frischen Klonen ist --syncdb notwendig, da sonst notwendige Tabellen in der Datenbank fehlen!

- WICHTIG: Bitte 1x lokal: "pip install django-bootstrap-v5" + "pip install pillow" ausführen um Bootstrap und Pillow nutzen zu können!

WINDOWS Befehle:
python manage.py migrate --run-syncdb
python manage.py createsuperuser
python manage.py loaddata Users.json --app Rating 
python manage.py loaddata Beertypes.json --app Rating
python manage.py loaddata Breweries.json --app Rating
python manage.py loaddata Beers.json --app Rating
python manage.py loaddata Recommendations.json --app Rating
python manage.py loaddata news_entries.json --app Rating
