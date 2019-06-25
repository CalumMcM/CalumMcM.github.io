#############################
# Powered by Dark Sky       #
# Author: Calum McMeekin    #
#############################

import urllib2
import json
from datetime import datetime

ClothesDict = {'StreetShoes':True, 'Gloves':False,'Wellies':False,'StreetTrousers':True,'WaterproofJacket':False,'Jumper':False,'Sunglasses':False,'DuvetJacket':False,'WaterproofTrousers':False,'SuncreamFactor30':False,'SuncreamFactor50':False,'Tshirt':True,'WoolyHat':False,'Thermals':False}
global BoulderScore

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKLIGHTBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    GREENUNDERBLACK = '\033[102m'
    REDUNDERBLACK = '\033[101m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def getAPIData(location):
    #keyGeolocation = 'b71199c8872647f888aee90d767ae10b' #For OpenCage geolocation
    #keyDarkSky = '2aa80cccb9cabf5848fd5ac03f2fc760' #For Dark Sky API
    urlGeolocation = 'https://api.opencagedata.com/geocode/v1/json?q='+str(location)+'&key=b71199c8872647f888aee90d767ae10b'

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
    collectedData = {'rainsh':[], 'cloudCover':[], 'appTempsh':[], 'preciph':[], 'windsh':[], 'uvIndex':[], 'timesh':[]}
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
        Hourtime = ((datetime.fromtimestamp(Curtime)).strftime("%H:%M"))
        collectedData['timesh'].append(Hourtime)
        collectedData['uvIndex'].append(uv)
        collectedData['preciph'].append(precip)
        collectedData['rainsh'].append(rain)
        collectedData['appTempsh'].append(appTemp)
        collectedData['cloudCover'].append(cloud)
        collectedData['windsh'].append(wind)
        if (curHour == HoursWanted):
            break
        else:
            curHour += 1

    averageTemps = sum(collectedData['appTempsh'])/len(collectedData['appTempsh'])            #Average Temperature for next 48h
    totalRainfall = sum(collectedData['rainsh'])                                              #Total rainfall in mm for next 48h
    highestPrecipProb = max(collectedData['preciph'])                                         #Highest precipitation probability
    RHP = collectedData['rainsh'][collectedData['preciph'].index(highestPrecipProb)]          #Rain for Highest Proability
    timeOfRHP = collectedData['timesh'][collectedData['preciph'].index(highestPrecipProb)] 
    #print (bcolors.UNDERLINE + "\n\nSummary:\n\n" + bcolors.ENDC + Summary48h + "\nHighest amount of rainfall during an hour will be at " + timeOfRHP + ". With " + str(RHP) + "mm falling, and a chance of " + str(highestPrecipProb*100) + "%\nThe total rainfall will be: " + str(totalRainfall) + "mm\nThe average temperature will be: " + str(round(averageTemps,1)) + u"\u00b0C\n")
    
    return collectedData

#Extracts required data from Dark Sky API data for number of days given
#Returns a dictionary holding this extracted data 
def breakDownData8(dataDark, days):
    collectedData = {'dates':[],'tempAppMin':[],'tempAppMax':[],'winds':[],'cloudCover':[],'rains':[],'precipProbs':[], 'uvIndex':[]} #Dictionary holding all collected data
    dailyDictionary = dataDark["daily"]
    summary = dailyDictionary["summary"]
    dataDaily = dailyDictionary["data"]
    collectedData['Summary'] = summary

    curDay = 1
    #print (bcolors.UNDERLINE + "\n\nSummary:\n\n" + bcolors.ENDC)
    #print (bcolors.HEADER + bcolors.UNDERLINE + "Day\t\tRainfall (mm)\tHighest Apparent Temperature (" + u"\u00b0C" + ")\tLowest Apparent Temperature ("+ u"\u00b0C" + ")\tCloudCover (%)" + bcolors.ENDC + "\n")
    for item in dataDaily:
        tempMax = item["apparentTemperatureMax"]
        tempMin = item["apparentTemperatureMin"]
        wind = item["windSpeed"]
        uv = item["uvIndex"]
        cloudCover = item["cloudCover"]
        rain = item["precipIntensityMax"]
        precipProb = item["precipProbability"]
        time = item["sunriseTime"]
        day = (datetime.fromtimestamp(time)).strftime("%A")
        collectedData['dates'].append(day)
        collectedData['rains'].append(rain)
        collectedData['uvIndex'].append(uv)
        collectedData['precipProbs'].append(precipProb)
        collectedData['cloudCover'].append(cloudCover)
        collectedData['tempAppMax'].append(tempMax)
        collectedData['tempAppMin'].append(tempMin)
        collectedData['winds'].append(wind)
        if (curDay == days):
            break
        else:
            curDay += 1
    dayOfMaxRain = collectedData['dates'][collectedData['rains'].index(max(collectedData["rains"]))]
    dayOfMaxTemp = collectedData['dates'][collectedData['tempAppMax'].index(max(collectedData["tempAppMax"]))]
    dayOfMinTemp = collectedData['dates'][collectedData['tempAppMin'].index(max(collectedData["tempAppMin"]))]
    #print ("\n\n" + summary + "\nHighest amount of rainfall on a given day will be " + str(max(collectedData["rains"])) + "mm on " + str(dayOfMaxRain) + ".\nHighest temperature will be " + str(max(collectedData["tempAppMax"])) + u"\u00b0C" + " on " + str(dayOfMaxTemp) + ". Lowest temperature will be " + str(min(collectedData["tempAppMin"])) + u"\u00b0C" + " on " + str(dayOfMinTemp) + ".\n")
    return collectedData

def recommenderH(collectedData):
    BoulderScore = 9
    averagetemp = sum(collectedData['appTempsh'])/len(collectedData['appTempsh'])
    #Cold temperature filter
    if (averagetemp < 12):
        ClothesDict['Jumper'] = True
        BoulderScore += 6
        if (averagetemp < 6 and (len([RainHour for RainHour in collectedData['rainsh'] if RainHour >= 0.19]) == 0)):
            ClothesDict['DuvetJacket'] = True
            BoulderScore -=6
        elif (averagetemp < 1):
            BoulderScore -= 6
            ClothesDict['WoolyHat'] = True
            ClothesDict['DuvetJacket'] = True
            if (min(collectedData['appTempsh']) < -2):
                BoulderScore -= 2
                ClothesDict['Gloves'] = True
                ClothesDict['WaterproofJacket'] = True
            if (averagetemp < -5):
                BoulderScore -= 4
                ClothesDict['Thermals'] = True
    #Warm temperature filter
    if(sum(collectedData['appTempsh'])/len(collectedData['appTempsh']) >= 12): #Averagetemp is > 15
        BoulderScore += 4
        if(sum(collectedData['appTempsh'])/len(collectedData['appTempsh']) >= 25): #Averagetemp is > 25
            BoulderScore += 8
    #Rain filter
    if (len([RainHour for RainHour in collectedData['rainsh'] if RainHour >= 0.19]) > 0): #List comprehension to check if there is ever an hour with >0.19mm of rain
        BoulderScore -= 1
        if (len([RainHour for RainHour in collectedData['rainsh'] if RainHour >= 0.2]) > 0):
            ClothesDict['WaterproofJacket'] = True
            BoulderScore -= 30
            if (len([RainHour for RainHour in collectedData['rainsh'] if RainHour >= 3]) > 0):
                BoulderScore -= 10
                ClothesDict['Wellies'] = True
                ClothesDict['WaterproofTrousers'] = True
    #CloudCover filter
    if ( (sum(collectedData['cloudCover'])/len(collectedData['cloudCover'])) < 0.4): #average cloud cover > 30% and uvIndex >6
        ClothesDict['Sunglasses'] = True
    #UV filter
    if (len([uvHour for uvHour in collectedData['uvIndex'] if uvHour >7])):
        ClothesDict['SuncreamFactor30']
        if (len([uvHour for uvHour in collectedData['uvIndex'] if uvHour >9])):
            ClothesDict['SuncreamFactor50']
    return BoulderProcessor(BoulderScore)

def recommenderD(collectedData, days):
    #Cold Filter
    if (len([minTemp for minTemp in collectedData['tempAppMin'] if minTemp < 15]) > 0):
        ClothesDict["Jumper"] = True
        if (len([minTemp for minTemp in collectedData['tempAppMin'] if minTemp < 10]) > 0 ):
            ClothesDict["DuvetJacket"] = True
            if (len([minTemp for minTemp in collectedData['tempAppMin'] if minTemp < 5]) > 0):
                ClothesDict["WoolyHat"] = True
                ClothesDict["WaterproofJacket"] = True
                if (len([minTemp for minTemp in collectedData['tempAppMin'] if minTemp < 0]) > 0):
                    ClothesDict["Thermals"] = True
                    ClothesDict["Gloves"] = True
    #Rain filter
    if (len([RainHour for RainHour in collectedData['rains'] if RainHour >= 0.2]) > 0):
        ClothesDict["WaterproofJacket"] = True
        if (len([RainHour for RainHour in collectedData['rains'] if RainHour >= 1.5]) > 0):
            ClothesDict["WaterproofTrousers"] = True
            if (len([RainHour for RainHour in collectedData['rains'] if RainHour >= 3]) > 0):
                ClothesDict["Wellies"] = True
    #UV Filter
    if (len([uvHour for uvHour in collectedData['uvIndex'] if uvHour >7])):
        ClothesDict['SuncreamFactor30']
        if (len([uvHour for uvHour in collectedData['uvIndex'] if uvHour >9])):
            ClothesDict['SuncreamFactor50']
    #CloudCover Filter
    if (len([cloudCover for cloudCover in collectedData['cloudCover'] if cloudCover<0.35])>0): #average cloud cover > 30% and uvIndex >6
        ClothesDict['Sunglasses'] = True
    #Boulder Judgment
    Consecutives = 0
    BoulderJudgment = bcolors.WARNING + "Never dry rock" + bcolors.ENDC
    BestDays = []
    for curDay in range(days):
        if (collectedData["rains"][curDay] <= 0.3 and collectedData['tempAppMin'][curDay] > -3 and collectedData['tempAppMax'][curDay] < 25):
            Consecutives += 1
        else:
            Consecutives = 0
        if Consecutives >= 2:
            BestDays.append(collectedData["dates"][curDay])
    if len(BestDays)>0:
        BoulderJudgment = bcolors.OKGREEN + "Possible bouldering on "
        for bestDay in BestDays:
            BoulderJudgment = BoulderJudgment + str(bestDay) + " "
        BoulderJudgment = BoulderJudgment + bcolors.ENDC
    return BoulderJudgment

def BoulderProcessor(BoulderScore):
    switch = {
        #Dry ratings
        9: bcolors.OKGREEN + "PERFECT" + bcolors.ENDC,
        3: bcolors.OKGREEN + "A tad cold but dry" + bcolors.ENDC,
        1: bcolors.OKGREEN + "Very cold but dry" + bcolors.ENDC,
        -3: bcolors.WARNING + "Extremely cold but dry" + bcolors.ENDC,
        15: bcolors.OKGREEN + "PERFECT" + bcolors.ENDC,
        13: bcolors.OKGREEN + "Very warm but dry" + bcolors.ENDC,
        21: bcolors.WARNING + "Extremely warm but dry" + bcolors.ENDC,
        #Damp ratings
        8: bcolors.OKLIGHTBLUE + "Mild but damp" + bcolors.ENDC,
        2: bcolors.OKLIGHTBLUE + "A tad cold and damp" + bcolors.ENDC,
        0: bcolors.WARNING + "Very cold and damp" + bcolors.ENDC,
        -2: bcolors.FAIL + "Extremely cold and wet" + bcolors.ENDC,
        14: bcolors.OKLIGHTBLUE + "Warm but damp" + bcolors.ENDC,
        12: bcolors.WARNING + "Very warm and damp" + bcolors.ENDC,
        20: bcolors.FAIL + "Extremely warm and damp" + bcolors.ENDC,
        #Wet ratings
        -22: bcolors.OKBLUE + "Wet but mild, look for overhang" + bcolors.ENDC,
        -28: bcolors.FAIL + "Its just not gonna work out i'm afraid" + bcolors.ENDC,
        -30: bcolors.WARNING + "Wet and very cold" + bcolors.ENDC,
        -32: bcolors.FAIL + "Put the kettle on as there's no chance of a send" + bcolors.ENDC,
        -16: bcolors.OKBLUE + "Warm and wet, look for overhang" + bcolors.ENDC,
        -18: bcolors.WARNING + "Very warm and wet, overhang required" + bcolors.ENDC,
        -10: bcolors.FAIL + "Extremely warm and wet" + bcolors.ENDC,
        #Soaking ratings
        -38: bcolors.FAIL + "Extremely wet and cold" + bcolors.ENDC,
        -40: bcolors.FAIL + "Extremely wet and very cold" + bcolors.ENDC,
        -42: bcolors.REDUNDERBLACK + "Don't even think of getting the send in" + bcolors.ENDC,
        -26: bcolors.FAIL + "Extrememly wet and warm" + bcolors.ENDC,
        -20: bcolors.REDUNDERBLACK + "Why are you even asking?" + bcolors.ENDC
    } 
    return switch.get(BoulderScore, "Unprecidented Boulder Score of: " + str(BoulderScore))

def output(BoulderJudgement):
    pack = []
    leave = []
    print bcolors.HEADER + "Boulder Judgment: " + BoulderJudgement + "\n"
    for clothingItem in ClothesDict:
        if ClothesDict[clothingItem]:
            pack.append(clothingItem)
        else:
            leave.append(clothingItem)
    print bcolors.UNDERLINE + "You should PACK:" + bcolors.ENDC
    for item in pack:
        print bcolors.OKGREEN + item + bcolors.ENDC
    print bcolors.UNDERLINE + "\nYou should LEAVE:" + bcolors.ENDC + ""
    for item in leave:
        print bcolors.WARNING + item + bcolors.ENDC

def outputAPI(BoulderJudgement, collectedData):
    collectedData["BoulderJudgment"] = BoulderJudgement
    print collectedData
    return collectedData

def main(location, days, hours):
    dataDark = getAPIData(location)
    if (days <=2):
        collectedData = breakDownData50(dataDark, hours)
        BoulderJudgement = recommenderH(collectedData)
    else:
        collectedData = breakDownData8(dataDark, days)
        BoulderJudgement = recommenderD(collectedData, days)
    outputAPI(BoulderJudgement, collectedData)
if __name__ == "__main__":
    main("EH39JN", 1, 3)