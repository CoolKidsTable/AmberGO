from lxml import html
import requests

def getVehicleImage(make="ford",model="focus",year="2012"):
    response = requests.get("https://www.autobytel.com/{}/{}/{}/pictures/".format(make,model,year))
    root = html.fromstring(response.content)
    imgserch = root.xpath("//a[contains(@id,'imageThumb')]/div/img")
    picSrcList = []
    for pic in range(len(imgserch)):
        if pic == 8:
            break
        picSrcList.append("https:"+imgserch[pic].attrib["src"])

    return picSrcList

def milestoMeters(inMiles):
    return inMiles * 1609.344

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
    response = requests.get(pageLink.format(make,model,year))
    root = html.fromstring(response.content)
    fuelCap = root.xpath("//div[@class='subnav-content']/ul/li/ul/li/span[contains(text(),'Fuel tank capacity:')]/following-sibling::span[contains(@class,'smaller') and contains(@class,'bold') and contains(@class,'float-right')]")
    cityMPG = root.xpath("//div[@class='subnav-content']/ul/li/ul/li/span[contains(text(),'City:')]/following-sibling::span[contains(@class,'smaller') and contains(@class,'bold') and contains(@class,'float-right')]")
    hwMPG = root.xpath("//div[@class='subnav-content']/ul/li/ul/li/span[contains(text(),'Highway:')]/following-sibling::span[contains(@class,'smaller') and contains(@class,'bold') and contains(@class,'float-right')]")
    fuelCap = float(fuelCap[0].text.split("gal")[0])
    cityMPG = float(cityMPG[0].text.strip(" mpg"))
    hwMPG = float(hwMPG[0].text.strip(" mpg"))
    searchRadius = (cityMPG + hwMPG) / 2 * fuelCap
    return milestoMeters(searchRadius)

def fuelEconomyVehicleImage(make="ford",model="focus",year="2012"):
    pageLink = f"https://www.fueleconomy.gov/feg/bymodel/{year}_{make}_{model}.shtml"
    response = requests.get(pageLink)
    root = html.fromstring(response.content)
    vehicleImages = [f"https://www.fueleconomy.gov{image.attrib['src']}" for image in root.xpath('//div[@id="main-content"]/div[@class="row"]/table/tbody/tr/td[contains(@class,"vphoto")]/img[not(@src[contains(.,"Electric")])]')]
    return vehicleImages

def fuelEconomySearchRadius(make="ford",model="focus",year="2012"):
    baseURL = "https://www.fueleconomy.gov/feg"
    pageLink = f"{baseURL}/bymodel/{year}_{make}_{model}.shtml"
    response = requests.get(pageLink)
    root = html.fromstring(response.content)
    vehicleExt = root.xpath('//a[@class="ymm" and not(contains(text(),"Electric"))]')[0].attrib["href"].replace("..","")
    response = requests.get(f"{baseURL}{vehicleExt}")
    root = html.fromstring(response.text)
    finalPageExt = root.xpath('//a[@role="button" and contains(@href,"action=sbs&id")]')[0].attrib["href"]
    response = requests.get(f"https://www.fueleconomy.gov{finalPageExt}")
    root = html.fromstring(response.content)
    mpg = float(root.xpath('//td[@class="combinedMPG"]')[0].text_content().split(":")[1])
    tankSize = root.xpath('//td[preceding-sibling::th[text()="Tank Size"]]')[0].text
    print(tankSize)
    tankSize = tankSize.split(" ")[0]
    print("SANDWHICH")
    print(tankSize)
    print("SAMMICH")
    tankSize = float(tankSize)
    searchRadius = round(mpg * tankSize,2)
    return milestoMeters(searchRadius)
