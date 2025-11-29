import argparse
import requests

class Brewery:
    def __init__(self, id: str, name: str, brewery_type: str, city: str, state: str, country: str):
        self.id = id
        self.name = name
        self.brewery_type = brewery_type
        self.city = city
        self.state = state
        self.country = country

    def __str__(self):
        return f"{self.name} ({self.brewery_type}) - {self.city}, {self.state}, {self.country}"


parser = argparse.ArgumentParser()
parser.add_argument("--city", type=str, help="Nazwa miasta do filtrowania wyników")
args = parser.parse_args()

base_url = "https://api.openbrewerydb.org/v1/breweries"

if args.city:
    url = f"{base_url}?per_page=20&by_city={args.city}"
else:
    url = f"{base_url}?per_page=20"

response = requests.get(url)
data = response.json()

browary = []

for item in data:
    browary.append(
        Brewery(
            id=item.get("id"),
            name=item.get("name"),
            brewery_type=item.get("brewery_type"),
            city=item.get("city"),
            state=item.get("state"),
            country=item.get("country"),
        )
    )

for b in browary:
    print(b)
