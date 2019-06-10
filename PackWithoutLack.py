import urllib2
import json

"""
keyGeolocation = 'b71199c8872647f888aee90d767ae10b' #For OpenCage geolocation
keyDarkSky = '2aa80cccb9cabf5848fd5ac03f2fc760' #For Dark Sky API
urlGeolocation = 'https://api.opencagedata.com/geocode/v1/json?q=G630RE&key=b71199c8872647f888aee90d767ae10b'

json_objGeo = urllib2.urlopen(urlGeolocation)
dataGeo = json.load(json_objGeo)
"""
with open('geoResult.txt') as json_file: #Temporary use of reading the geo result to avoid constant messaging
    dataGeo = json.load(json_file)

for item in dataGeo['results']:
    pos = item["geometry"]
    lat = pos["lat"]
    lng = pos["lng"]

"""
urlDarkSky = 'https://api.darksky.net/forecast/2aa80cccb9cabf5848fd5ac03f2fc760/' + str(lat) + ',' + str(lng) 

json_obj = urllib2.urlopen(urlDarkSky)

dataDark = json.load(json_obj)
"""

with open('darkResult.txt') as json_file: #Temporary use of reading the dark result to avoid constant messaging
    dataDark = json.load(json_file)

hourlyDictionary = (dataDark["hourly"])
Summary48h = hourlyDictionary["summary"]
data48h = hourlyDictionary["data"]
print data48h["currently"]
rains48h = []

#time = data48h["summary"]

"""
    print item
    if item == 'data':
        hourlyData = item
    """

