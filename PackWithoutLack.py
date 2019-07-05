#############################
# Powered by Dark Sky       #
# Author: Calum McMeekin    #
#############################
import sys
import urllib2
import json
from datetime import datetime
from flask import Flask
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)


@app.route("/main/<location>/<daysS>/<hoursS>")
def main(location, daysS, hoursS):
    ClothesDict = {'BoulderJudgement':'','Casual Shoes':'True','Buff':'False','Sun Hat':'False','Shorts':'False','Gloves':'False','Wellies':'False','Trainers':'False','Jeans':'True','Jumper':'False','Sunglasses':'False','Duvet Jacket':'False','Waterproof Jacket':'False','Waterproof Trousers':'False','Suncream Facter 30':'False','Suncream Facter 50':'False','T-shirt':'True','Wooly hat':'False','Thermals':'False'}
    days = int(daysS)
    hours = int(hoursS)
    dataDark = getAPIData(location)
    if (days <=2):
        collectedData = breakDownData50(dataDark, hours, ClothesDict)
        BoulderJudgement = recommenderH(collectedData, ClothesDict)
    else:
        collectedData = breakDownData8(dataDark, days, ClothesDict)
        BoulderJudgement = recommenderD(collectedData, days, ClothesDict)
    ClothesDict['BoulderJudgement'] = BoulderJudgement
    return json.dumps(ClothesDict)


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
def breakDownData50(dataDark, HoursWanted, ClothesDict):
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
    summary = Summary48h + " Highest amount of rainfall during an hour will be at " + timeOfRHP + ". With " + str(RHP) + "mm falling, and a chance of " + str(highestPrecipProb*100) + "%<br>The total rainfall will be: " + str(totalRainfall) + "mm<br>The average temperature will be: " + str(round(averageTemps,1)) + "C"
    ClothesDict['summary'] = summary
    return collectedData

#Extracts required data from Dark Sky API data for number of days given
#Returns a dictionary holding this extracted data
def breakDownData8(dataDark, days, ClothesDict):
    collectedData = {'dates':[],'tempAppMin':[],'tempAppMax':[],'winds':[],'cloudCover':[],'rains':[],'precipProbs':[], 'uvIndex':[]} #Dictionary holding all collected data
    dailyDictionary = dataDark["daily"]
    summary8 = dailyDictionary["summary"]
    dataDaily = dailyDictionary["data"]
    collectedData['Summary'] = summary8
    forecastDict = {'days':[], 'rains':[], 'tempMaxs':[], 'tempMins':[], 'cloudCovers':[]}
    curDay = 1
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
        forecastDict['days'].append(day)
        forecastDict['rains'].append(rain)
        forecastDict['tempMaxs'].append(tempMax)
        forecastDict['tempMins'].append(tempMin)
        forecastDict['cloudCovers'].append(cloudCover)
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
    summary = summary8 + " Highest amount of rainfall on a given day will be " + str(max(collectedData["rains"])) + "mm on " + str(dayOfMaxRain) + ".<br>Highest temperature will be " + str(max(collectedData["tempAppMax"])) + "C" + " on " + str(dayOfMaxTemp) + ". Lowest temperature will be " + str(min(collectedData["tempAppMin"])) + "C" + " on " + str(dayOfMinTemp) + "."
    ClothesDict['summary'] = summary
    ClothesDict['forecast'] = forecastDict
    return collectedData

def recommenderH(collectedData, ClothesDict):
    BoulderScore = 9
    averagetemp = sum(collectedData['appTempsh'])/len(collectedData['appTempsh'])
    #Cold temperature filter
    if (averagetemp < 16):
        ClothesDict['Jumper'] = 'True'
        BoulderScore += 6
        if (averagetemp < 6 and (len([RainHour for RainHour in collectedData['rainsh'] if RainHour >= 0.19]) == 0)):
            ClothesDict['Duvet Jacket'] = 'True'
            BoulderScore -=4
        elif (averagetemp < 1):
            BoulderScore -= 6
            ClothesDict['Wooly hat'] = 'True'
            ClothesDict['Duvet Jacket'] = 'True'
            if (min(collectedData['appTempsh']) < -2):
                BoulderScore -= 2
                ClothesDict['Gloves'] = 'True'
                ClothesDict['Waterproof Jacket'] = 'True'
            if (averagetemp < -5):
                BoulderScore -= 4
                ClothesDict['Thermals'] = 'True'
    #Warm temperature filter
    if(sum(collectedData['appTempsh'])/len(collectedData['appTempsh']) >= 16): #Averagetemp is > 15
        BoulderScore += 100
        ClothesDict['Shorts'] = 'True'
        if(sum(collectedData['appTempsh'])/len(collectedData['appTempsh']) >= 25): #Averagetemp is > 25
            BoulderScore += 8
            if(sum(collectedData['appTempsh'])/len(collectedData['appTempsh']) >= 30): #Averagetemp is > 25
                BoulderScore += 100
    #Rain filter
    if (len([RainHour for RainHour in collectedData['rainsh'] if RainHour >= 0.05]) > 0): #List comprehension to check if there is ever an hour with >0.19mm of rain
        BoulderScore -= 1
        if (len([RainHour for RainHour in collectedData['rainsh'] if RainHour >= 0.1]) > 0):
            ClothesDict['Waterproof Jacket'] = 'True'
            BoulderScore -= 30
            if (len([RainHour for RainHour in collectedData['rainsh'] if RainHour >= 1]) > 0):
                ClothesDict['Trainers'] = 'True'
                BoulderScore -= 30
                if (len([RainHour for RainHour in collectedData['rainsh'] if RainHour >= 2]) > 0):
                    ClothesDict['Waterproof Trousers'] = 'True'
                    if (len([RainHour for RainHour in collectedData['rainsh'] if RainHour >= 3]) > 0):
                        BoulderScore -= 30
                        ClothesDict['Wellies'] = 'True'
    #Wind filter
    if(len([wind for wind in collectedData['windsh'] if wind >30])>0):
        ClothesDict['Buff'] = 'True'
    #CloudCover filter
    if ( (sum(collectedData['cloudCover'])/len(collectedData['cloudCover'])) < 0.4): #average cloud cover > 30% and uvIndex >6
        ClothesDict['Sunglasses'] = 'True'
        if ( (sum(collectedData['cloudCover'])/len(collectedData['cloudCover'])) < 0.3):
            ClothesDict['Sun Hat'] = 'True'
    #UV filter
    if (len([uvHour for uvHour in collectedData['uvIndex'] if uvHour >6])>0):
        ClothesDict['Suncream Facter 30']
        if (len([uvHour for uvHour in collectedData['uvIndex'] if uvHour >8])>0):
            ClothesDict['Suncream Facter 50']

    return BoulderProcessor(BoulderScore)

def recommenderD(collectedData, days, ClothesDict):
    #Cold Filter

    if (len([minTemp for minTemp in collectedData['tempAppMin'] if minTemp < 16]) > 0):
        ClothesDict["Jumper"] = 'True'
        if (len([minTemp for minTemp in collectedData['tempAppMin'] if minTemp < 11]) > 0 ):
            ClothesDict["Duvet Jacket"] = 'True'
            if (len([minTemp for minTemp in collectedData['tempAppMin'] if minTemp < 5]) > 0):
                ClothesDict["Wooly hat"] = 'True'
                ClothesDict["Waterproof Jacket"] = 'True'
                if (len([minTemp for minTemp in collectedData['tempAppMin'] if minTemp < 0]) > 0):
                    ClothesDict["Thermals"] = 'True'
                    ClothesDict["Gloves"] = 'True'
    #Warm temperature filter
    if(len([maxTemp for maxTemp in collectedData['tempAppMax'] if maxTemp > 16])>0): #Averagetemp is > 15
        ClothesDict['Shorts'] = 'True'
    #Rain filter
    if (len([RainHour for RainHour in collectedData['rains'] if RainHour >= 0.2]) > 0):
        ClothesDict["Waterproof Jacket"] = 'True'
        if (len([RainHour for RainHour in collectedData['rains'] if RainHour >= 1]) > 0):
            ClothesDict["Trainers"] = 'True'
            if (len([RainHour for RainHour in collectedData['rains'] if RainHour >= 1.5]) > 0):
                ClothesDict["Waterproof Trousers"] = 'True'
                if (len([RainHour for RainHour in collectedData['rains'] if RainHour >= 3]) > 0):
                    ClothesDict["Wellies"] = 'True'
    #UV Filter
    if (len([uvHour for uvHour in collectedData['uvIndex'] if uvHour >6])>0):
        ClothesDict['Suncream Facter 30']
        if (len([uvHour for uvHour in collectedData['uvIndex'] if uvHour >8])>0):
            ClothesDict['Suncream Facter 50']
    #Wind filter
    if(len([wind for wind in collectedData['winds'] if wind >30])>0):
        ClothesDict['Buff'] = 'True'
    #CloudCover Filter
    if (len([cloudCover for cloudCover in collectedData['cloudCover'] if cloudCover<0.4])>0): #average cloud cover < 40% and uvIndex >6
        ClothesDict['Sunglasses'] = 'True'
        if (len([cloudCover for cloudCover in collectedData['cloudCover'] if cloudCover<0.3])>0):
            ClothesDict['Sun Hat'] = 'True'
    #Boulder Judgment
    Consecutives = 0
    BoulderJudgment = ""
    BestDays = []
    for curDay in range(days):
        if (collectedData["rains"][curDay] <= 0.3 and collectedData['tempAppMin'][curDay] > -3 and collectedData['tempAppMax'][curDay] < 25):
            Consecutives += 1
        else:
            Consecutives = 0
        if Consecutives >= 2:
            BestDays.append(collectedData["dates"][curDay])
    if len(BestDays)>0:
        for bestDay in BestDays:
            BoulderJudgment = BoulderJudgment + str(bestDay) + " "
    else:
        BoulderJudgment = 'Absolutely none of them'

    return BoulderJudgment

def BoulderProcessor(BoulderScore):
    switch = {
        #Key:
        #Green - Very good conditions, have a good climb
        #skyblue - A little damp but should be fine for rocks that are semi-sheltered
        #Blue - Conditions are very wet - unless you are cave climbing/very overhanging you wont get a climb in
        #Warning - Conditions are dangerous but there is a chance of a climb - proceed with caution
        #dark red (89243A) - Dangerous conditions - a climb is not recommended
        #Red - Very dangerous conditions - Do not proceed to climb
        #Dry ratings
        15:  "Green|Mild and dry",
        11:  "Green|Chilly yet dry",
        5:   "Green|Cold but dry",
        3:   "Green|Very cold but dry",
        -1:  "Warning|Extremely cold but dry",
        109:  "Green|Warm and dry",
        117:  "Warning|Very warm but dry",
        217:  "89243A|Extremely warm and dry",
        #Damp ratings
        14:  "skyblue|Mild but damp",
        10:  "skyblue|A tad cold and damp",
        4:  "skyblue|Cold and damp",
        2: "89243A|Very cold and wet",
        -2: "89243A|Extremely cold and damp",
        108: "skyblue|Warm and damp",
        116: "skyblue|Very warm and damp",
        216:"Red|Extremely warm and damp",
        #Wet ratings
        -16: "Blue|Wet but mild, look for overhang",
        -20: "89243A|Wet and chilly",
        -26: "89243A|Wet and cold",
        -28: "Red|Forget it, put the kettle on",
        -32: "Red|Extremely cold and wet",
         78: "Blue|Very warm and wet, overhang required",
         86:" Blue|Find a cave or find a kettle",
        186: "Red|Extremely warm and wet",
        #Soaking ratings
        -46: "89243A|Extremely wet yet mild",
        -50: "89243A|Extremely wet and chilly",
        -56: "Red|Slip N slide conditions",
        -58: "Red|Don't even think of getting the send in",
        -62: "Red|Why are you even asking?",
        48: "Red|Super Soaker conditions",
        56: "Red|Very warm. Very Wet.",
        156: "Red|Extremely warm. Very wet. Poor Combo.",
        #Thunderstorm ratins
        -76: "Blue|Thunderstorm rains but mild",
        -80: "Blue|Thunderstorm rains and chilly",
        -86: "89243A|Thunderstorm rains and cold",
        -88: "89243A|Thunderstorm rains and very cold",
        -92: "Red|Thunderstorm rains and extremely cold",
        -18: "Blue|Tropical Thunderstorm conditions",
        26: "89243A|Carribean Thunderstorm conditions",
        126: "Red|Amazonian Thunderstorm conditions",
    }
    return switch.get(BoulderScore, str(BoulderScore))

if __name__ == "__main__":
    app.run()
