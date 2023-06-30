#!/bin/zsh

directory="dumps"
fileextension=".json"
date="$(date +"%Y%m%d")"


filename="alldata"
fullpath="${directory}/${date}_${filename}${fileextension}"
echo $fullpath
python3 manage.py dumpdata Rating > $fullpath


filename="beers"
fullpath="${directory}/${date}_${filename}${fileextension}"
echo $fullpath
python3 manage.py dumpdata Rating.beer > $fullpath

filename="breweries"
fullpath="${directory}/${date}_${filename}${fileextension}"
echo $fullpath
python3 manage.py dumpdata Rating.brewery > $fullpath

filename="beertypes"
fullpath="${directory}/${date}_${filename}${fileextension}"
echo $fullpath
python3 manage.py dumpdata Rating.beertype > $fullpath

filename="recommendations"
fullpath="${directory}/${date}_${filename}${fileextension}"
echo $fullpath
python3 manage.py dumpdata Rating.recommendation > $fullpath


