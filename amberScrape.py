from lxml import html
import requests

def getVehicleImage(make="ford",model="focus",year="2012"):
    response = requests.get("https://www.autobytel.com/{}/{}/{}/pictures/".format(make,model,year))
    root = html.fromstring(response.content)
    imgserch = root.xpath("//a[contains(@id,'imageThumb')]/div/img")
    return "https:"+imgserch[0].attrib["src"]

def getCenterCoordinates(address="1600+Amphitheatre+Parkway",city="Mountain+View",state="CA",country="US"):
    address = address.replace(" ","+")
    city = city.replace(" ","+")
    address = "{},+{},+{}".format(address,city,state)
    components="country:{}".format(country)
    base_url = "https://maps.googleapis.com/maps/api/geocode/json?address={}&components={}&key={}".format(address,components,"AIzaSyDTdSCWaM8oDJgvLOklr5c2jlSnEDC6Ru4")
    response = requests.get(base_url)
    locationInfo = response.json()["results"][0]["geometry"]["location"]
    return [locationInfo["lat"],locationInfo["lng"]]

def getSearchRadius(make="ford",model="focus",year="2012"):
    pageLink = "https://www.autobytel.com/{}/{}/{}/specifications/"
    make = "ford"
    model = "focus"
    year = 2012
    response = requests.get(pageLink.format(make,model,year))
    root = html.fromstring(response.content)
    fuelCap = root.xpath("//div[@class='subnav-content']/ul/li/ul/li/span[contains(text(),'Fuel tank capacity:')]/following-sibling::span[contains(@class,'smaller') and contains(@class,'bold') and contains(@class,'float-right')]")
    cityMPG = root.xpath("//div[@class='subnav-content']/ul/li/ul/li/span[contains(text(),'City:')]/following-sibling::span[contains(@class,'smaller') and contains(@class,'bold') and contains(@class,'float-right')]")
    hwMPG = root.xpath("//div[@class='subnav-content']/ul/li/ul/li/span[contains(text(),'Highway:')]/following-sibling::span[contains(@class,'smaller') and contains(@class,'bold') and contains(@class,'float-right')]")
    fuelCap = float(fuelCap[0].text.split("gal")[0])
    cityMPG = float(cityMPG[0].text.strip(" mpg"))
    hwMPG = float(hwMPG[0].text.strip(" mpg"))
    searchRadius = (cityMPG + hwMPG) / 2 * fuelCap
    searchRadiusInMeters = searchRadius * 1609.344
    return searchRadiusInMeters