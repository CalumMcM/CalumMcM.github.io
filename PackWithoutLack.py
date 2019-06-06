import urllib2
import json

keyGeolocation = 'b71199c8872647f888aee90d767ae10b' #For OpenCage geolocation
keyDarkSky = '2aa80cccb9cabf5848fd5ac03f2fc760' #For Dark Sky API
urlGeolocation = 'https://api.opencagedata.com/geocode/v1/json?q=G630RE&key=b71199c8872647f888aee90d767ae10b'
urlDarkSky = 'https://api.darksky.net/forecast/2aa80cccb9cabf5848fd5ac03f2fc760/37.8267,-122.4233'
json_objGeo = urllib2.urlopen(urlGeolocation)
dataGeo = json.load(json_objGeo)

for item in dataGeo['results']:
    pos = item["geometry"]
    lat = pos["lat"]
    lng = pos["lng"]
print lat
print lng
"""
json_obj = urllib2.urlopen(urlDarkSky)

data = json.load(json_obj)
print data


for item in data['hourly']:
    if item == 'data':
        for key in data:
            print data[key]
    i += 1
    weatherType = item['main']
    weatherSeverity = item['description']
"""