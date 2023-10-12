from geopy.geocoders import Nominatim
import os
import re
def getCountryCode(latlong):
    try:
        geolocator = Nominatim(user_agent=os.getenv("NOMATIM_USER_AGENT",""))
        location=geolocator.reverse(latlong)
        address = location.raw['address']
    except:
        return None
    
    return address.get("country_code", None)
def isValidString(string):
    if string is None:
        return False
    if string == "":
        return False
    return True

def removeHTMLParametres(string):
    return re.sub(r"(\?|\&)([^=]+)\=([^&]+)", "", string)

def domainExtractor(url):
    return re.search(r"(?:https?:\/\/)?(?:[^@\n]+@)?(?:www\.)?([^:\/\n?]+)", url).group(1)