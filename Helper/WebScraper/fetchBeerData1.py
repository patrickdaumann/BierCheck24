import requests, time, csv
from bs4 import BeautifulSoup


class beerdata:

    def __init__(self, url: str) -> None:
        self.url = url

        # leeres dict initialisieren
        self.data = {}

    def parse(self) -> None:
        self.response = requests.get(self.url)
        self.html_content = self.response.text

    def scrapename(self) -> None:
        soup = BeautifulSoup(self.html_content, 'html.parser')
        element = soup.find('span', itemprop='name')
        bier_name = element.get_text(strip=True)
        self.data["Name"] = bier_name

    def scrape(self, searchstring: str, attributename:str) -> None:
        soup = BeautifulSoup(self.html_content, 'html.parser')
        element = soup.find('strong', class_=searchstring)
        
        if element:
            data = element.next_sibling.strip()
        else:
            data = "Error"
        
        self.data[attributename] = data

    def print(self):
        print(self.data)


searchstrings = {
    "Style": "bier_typ",
    "alcohol_content": "bier_alkohol",
    "original_gravity": "bier_stw",
    "recommended_serving_temperature": "bier_temp",
    "is_organic": "bier_bio",
    "clarity": "bier_filter",
    "is_gluten_free": "bier_glutenfrei"
}


with open("Helper/WebScraper/urls.txt", 'r') as file:
    urls = file.readlines()

beers = []

for url in urls:
    beer = beerdata(url=url.strip())
    beer.parse()

    beer.scrapename()
    for key, value in searchstrings.items():
        beer.scrape(searchstring=value, attributename=key)
    beer.print()
    beers.append(beer)




def exportiere_csv(beer_list, dateiname):
    # Definiere die Spaltenüberschriften basierend auf den Schlüsseln im ersten Eintrag
    spaltennamen = list(beer_list[0].data.keys())

    # Öffne die CSV-Datei im Schreibmodus
    with open(dateiname, mode='w', newline='') as datei:
        writer = csv.writer(datei)

        # Schreibe die Spaltenüberschriften
        writer.writerow(spaltennamen)

        # Schreibe die Daten für jedes Bier
        for beer in beer_list:
            daten = [beer.data[key] for key in spaltennamen]
            writer.writerow(daten)


#exportiere_csv(beers, "Helper/WebScraper/BeerExport.csv")
