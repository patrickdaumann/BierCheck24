# Install

```bash
git clone git@github.com:patrickdaumann/BierCheck24.git

cd BierCheck24

python3 manage.py runserver
python3 manage.py migrate --run-syncdb

python3 manage.py createsuperuser

python3 manage.py loaddata Beertypes.json --app Rating

python3 manage.py loaddata Breweries.json --app Rating

python3 manage.py loaddata Beers.json --app Rating

python3 manage.py runserver

```

- Nach einem frischen Klonen ist --syncdb notwendig, da sonst notwendige Tabellen in der Datenbank fehlen!

- Test
