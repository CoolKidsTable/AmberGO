from lxml import html
import requests

def main():
    make = "ford"
    model = "focus"
    year = "2012"
    BASE_URL = "https://www.fueleconomy.gov/ws/rest"
    MAKE_MODEL = "/ympg/shared/vehicles?year={}&make={}&model={}"
    response = requests.get(BASE_URL+MAKE_MODEL.format(year,make,model))
    
    roots = html.fromstring(response.content)
    milepergal = roots.xpath("//city08")
    barrels = roots.xpath("//barrels08")
    print(barrels[0].text)
    maxdis = float(milepergal[0].text) * (float(barrels[0].text) * 31.5)
    print(maxdis)
main()