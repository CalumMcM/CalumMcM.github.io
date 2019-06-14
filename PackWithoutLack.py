#############################
# Powered by Dark Sky       #
# Author: Calum McMeekin    #
#############################

import urllib2
import json
from datetime import datetime

def getAPIData():
    keyGeolocation = 'b71199c8872647f888aee90d767ae10b' #For OpenCage geolocation
    keyDarkSky = '2aa80cccb9cabf5848fd5ac03f2fc760' #For Dark Sky API
    urlGeolocation = 'https://api.opencagedata.com/geocode/v1/json?q=EH39JN&key=b71199c8872647f888aee90d767ae10b'

    json_objGeo = urllib2.urlopen(urlGeolocation)
    dataGeo = json.load(json_objGeo)
    """
    with open('geoResult.txt') as json_file: #Temporary use of reading the geo result to avoid constant messaging
        dataGeo = json.load(json_file)
    """
    for item in dataGeo['results']:
        pos = item["geometry"]
        lat = pos["lat"]
        lng = pos["lng"]

    urlDarkSky = 'https://api.darksky.net/forecast/2aa80cccb9cabf5848fd5ac03f2fc760/' + str(lat) + ',' + str(lng)
    json_obj = urllib2.urlopen(urlDarkSky)
    dataDark = json.load(json_obj)

    #with open('darkResult.txt') as json_file: #Temporary use of reading the dark result to avoid constant messaging
    #dataDark = json.load(json_file)

    return dataDark

def processData(dataDark):
    hourlyDictionary = (dataDark["hourly"])
    Summary48h = hourlyDictionary["summary"]
    data48h = hourlyDictionary["data"]

    rains48h = []
    temps48h = []
    times48h = []
    precip48h = []

    #Time comes in form  "seconds since midnight GMT on 1 Jan 1970"
    #print(datetime.utcfromtimestamp(Curtime).strftime('%Y-%m-%d %H:%M:%S'))

    for item in data48h:
        tempF = item["temperature"]
        rain = item["precipIntensity"]
        precip = item["precipProbability"]
        Curtime = item["time"]
        precip48h.append(precip)
        times48h.append(Curtime)
        rains48h.append(rain)
        temps48h.append(int(round((tempF -32) * 5/9)))

    averageTemps = sum(temps48h)/len(temps48h)          #Average Temperature for next 48h
    totalRainfall = sum(rains48h)                       #Total rainfall in mm for next 48h
    highestPrecipProb = max(precip48h)                  #Highest precipitation probability
    RHP = rains48h[precip48h.index(highestPrecipProb)]  #Rain for Highest Proability

    print Summary48h + "\nHighest amount of rainfall in an hour will be: " + str(RHP) + "mm, with a chance of: " + str(highestPrecipProb*100) + "%\nThe total rainfall will be: " + str(totalRainfall) + "\nThe average temperature will be: " + str(averageTemps)


def main():
    dataDark = getAPIData()
    processData(dataDark)

if __name__ == "__main__":
    main()
