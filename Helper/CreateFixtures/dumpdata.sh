#!/bin/zsh

directory="dumps"
filename=$(date +"%Y%m%d")_alldata.json
fullpath="${directory}/${filename}"

python3 manage.py dumpdata Rating > $fullpath