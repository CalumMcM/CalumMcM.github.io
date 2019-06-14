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
    for item in dataDark:
        print item
    return dataDark

def breakDownData50(dataDark, HoursWanted):
    hourlyDictionary = dataDark["hourly"]
    Summary48h = hourlyDictionary["summary"]
    data48h = hourlyDictionary["data"]
    
    rainsh = []
    tempsh = []
    timesh = []
    preciph = []
    cloudh = []

    #Time comes in form  "seconds since midnight GMT on 1 Jan 1970"
    #print(datetime.utcfromtimestamp(Curtime).strftime('%Y-%m-%d %H:%M:%S'))
    curHour = 0
    for item in data48h:
        tempF = item["temperature"]
        rain = item["precipIntensity"]
        precip = item["precipProbability"]
        cloud = item["cloudCover"]
        Curtime = item["time"]
        preciph.append(precip)
        timesh.append(Curtime)
        rainsh.append(rain)
        tempsh.append(int(round((tempF -32) * 5/9)))
        if (curHour == HoursWanted):
            break
        else:
            curHour += 1

    averageTemps = sum(tempsh)/len(tempsh)              #Average Temperature for next 48h
    totalRainfall = sum(rainsh)                         #Total rainfall in mm for next 48h
    highestPrecipProb = max(preciph)                    #Highest precipitation probability
    RHP = rainsh[preciph.index(highestPrecipProb)]      #Rain for Highest Proability

    print Summary48h + "\nHighest amount of rainfall in an hour will be: " + str(RHP) + "mm, with a chance of: " + str(highestPrecipProb*100) + "%\nThe total rainfall will be: " + str(totalRainfall) + "\nThe average temperature will be: " + str(averageTemps)
    collectedData = [averageTemps, totalRainfall, highestPrecipProb, RHP]
    return collectedData

def breakDownData8(dataDark, daysWanted):
    dailyDictionary = dataDark["daily"]
    collectedData = 0
    print dailyDictionary
    return collectedData

def recommender(collectedData):
    Jacket = False
    Jumper = False
    Sunglasses = False
    DuvetJacket = False
    WaterproofTrousers = False
    Suncream = False
    Tshirt = False
    WoolyHat = False


    print collectedData[0]

def main():
    days = int(raw_input("How many days will you be going away for? "))
    dataDark = getAPIData()
    if (days <=2):
        while (HoursWanted < 1 or HoursWanted > 50):
            HoursWanted = 0
            HoursWanted = int(raw_input("How many hours will you be away for? "))
            if (HoursWanted < 0 or HoursWanted > 50):
                print ("The number of hours must be between 0 and 50")
        collectedData = breakDownData50(dataDark, HoursWanted)
    else:
        collectedData = breakDownData8(dataDark, days)
    
    recommender(collectedData)

if __name__ == "__main__":
    main()
