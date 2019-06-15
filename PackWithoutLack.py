#############################
# Powered by Dark Sky       #
# Author: Calum McMeekin    #
#############################

import urllib2
import json
from datetime import datetime

ClothesDict = {'WaterproofJacket':False,'Jumper':False,'Sunglasses':False,'DuvetJacket':False,'WaterproofTrousers':False,'Suncream30':False,'Suncream50':False,'Tshirt':True,'WoolyHat':False,'Thermals':False}

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

    urlDarkSky = 'https://api.darksky.net/forecast/2aa80cccb9cabf5848fd5ac03f2fc760/' + str(lat) + ',' + str(lng) + '?units=si'
    json_obj = urllib2.urlopen(urlDarkSky)
    dataDark = json.load(json_obj)
    #with open('darkResult.txt') as json_file: #Temporary use of reading the dark result to avoid constant messaging
    #dataDark = json.load(json_file)

    return dataDark

#Extracts required data from Dark Sky API data for number of hours given
#Returns a dictionary holding this extracted data 
def breakDownData50(dataDark, HoursWanted):
    collectedData = {'tempsh':[], 'rainsh':[], 'cloudh':[], 'appTempsh':[], 'preciph':[], 'windsh':[], 'cloudCover':[], 'uvIndex':[]}
    hourlyDictionary = dataDark["hourly"]
    Summary48h = hourlyDictionary["summary"]
    data48h = hourlyDictionary["data"]
    collectedData['Summary'] = Summary48h

    #Time comes in form  "seconds since midnight GMT on 1 Jan 1970"
    #print(datetime.utcfromtimestamp(Curtime).strftime('%Y-%m-%d %H:%M:%S'))
    curHour = 0
    for item in data48h:
        appTemp = item["apparentTemperature"]
        rain = item["precipIntensity"]
        precip = item["precipProbability"]
        cloud = item["cloudCover"]
        uv = item['uvIndex']
        Curtime = item["time"]
        wind = item["windSpeed"]
        cloud = item['cloudCover']

        collectedData['uvIndex'].append(uv)
        collectedData['preciph'].append(precip)
        collectedData['timesh'].append(Curtime)
        collectedData['rainsh'].append(rain)
        collectedData['appTempsh'].append(appTemp)
        collectedData['cloudh'].append(cloud)
        collectedData['windsh'].append(wind)
        collectedData['cloudCover'].append(collectedData)
        if (curHour == HoursWanted):
            print item
            break
        else:
            curHour += 1

    averageTemps = sum(collectedData['tempsh'])/len(collectedData['tempsh'])                  #Average Temperature for next 48h
    totalRainfall = sum(collectedData['rainsh'])                                              #Total rainfall in mm for next 48h
    highestPrecipProb = max(collectedData['preciph'])                                         #Highest precipitation probability
    RHP = collectedData['rainsh'][collectedData['preciph'].index(highestPrecipProb)]          #Rain for Highest Proability

    print Summary48h + "\nHighest amount of rainfall in an hour will be: " + str(RHP) + "mm, with a chance of: " + str(highestPrecipProb*100) + "%\nThe total rainfall will be: " + str(totalRainfall) + "\nThe average temperature will be: " + str(averageTemps)
    
    return collectedData

#Extracts required data from Dark Sky API data for number of days given
#Returns a dictionary holding this extracted data 
def breakDownData8(dataDark, days):

    collectedData = {'tempAppMin':[],'tempAppMax':[],'winds':[],'cloudCovers':[],'rains':[],'precipProbs':[]} #Dictionary holding all collected data
    dailyDictionary = dataDark["daily"]
    summary = dailyDictionary["summary"]
    dataDaily = dailyDictionary["data"]
    collectedData['Summary'] = summary

    curDay = 1
    for item in dataDaily:
        tempMax = item["apparentTemperatureMax"]
        tempMin = item["apparentTemperatureMin"]
        wind = item["windSpeed"]
        cloudCover = item["cloudCover"]
        rain = item["precipIntensityMax"]
        precipProb = item["precipProbability"]

        collectedData['rains'].append(rain)
        collectedData['precipProbs'].append(precipProb)
        collectedData['cloudCovers'].append(cloudCover)
        collectedData['tempAppMax'].append(tempMax)
        collectedData['tempAppMin'].append(tempMin)
        collectedData['winds'].append(wind)
        if (curDay == days):
            break
        else:
            curDay += 1
    return collectedData

def recommenderH(collectedData):
    averagetemp = sum(collectedData['tempsh'])/len(collectedData['tempsh'])
    if (averagetemp < 15):
        ClothesDict['Jumper'] = True
        if (averagetemp < 5 and collectedData[1] < 0.2):
            ClothesDict['WoolyHat'] = True
            ClothesDict['DuvetJacket'] = True
            if (min(collectedData['tempsh']) < -5):
                ClothesDict['WaterproofJacket'] = True
            if (averagetemp < -13):
                ClothesDict['Thermals'] = True
    if (len([RainHour for RainHour in collectedData['rainsh'] if RainHour >= 0.19]) > 0): #List comprehension to check if there is ever an hour with >0.19mm of rain
        ClothesDict['WaterproofJacket'] = True
    if (sum(collectedData['cloudCover'])/len(collectedData['cloudCover']) < 0.3 and len([uvHour for uvHour in collectedData['uvIndex'] if uvHour > 6])>0): #average cloud cover > 30% and uvIndex >6
        ClothesDict['Sunglasses'] = True
    if (len([uvHour for uvHour in collectedData['uvIndex'] if uvHour >7])):
        ClothesDict['Suncream30']
        if (len([uvHour for uvHour in collectedData['uvIndex'] if uvHour >9])):
            ClothesDict['Suncream50']

def recommenderD(collectedData):

    print collectedData[0]

def main():
    """
    days = int(raw_input("How many days will you be going away for (including today)? "))
    night = bool(raw_input("Will you be outside during the night? (y/n) "))
    """
    days = 1
    dataDark = getAPIData()
    if (days <=2):
        HoursWanted = 0
        while (HoursWanted < 1 or HoursWanted > 50):
            #HoursWanted = int(raw_input("How many hours will you be away for? "))
            HoursWanted = 24
            if (HoursWanted < 0 or HoursWanted > 50):
                print ("The number of hours must be between 0 and 50")
        collectedData = breakDownData50(dataDark, HoursWanted)
    else:
        collectedData = breakDownData8(dataDark, days)
        recommenderD(collectedData)
    
    recommenderH(collectedData)

if __name__ == "__main__":
    main()
