ClothesDict = {'StreetShoes':'True', 'Gloves':'False','Wellies':'False','StreetTrousers':'True','WaterproofJacket':'False','Jumper':'False','Sunglasses':'False','DuvetJacket':'False','WaterproofTrousers':'False','SuncreamFactor30':'False','SuncreamFactor50':'False','Tshirt':'True','WoolyHat':'False','Thermals':'False'}
/*
class APICall{
    constructor(location, days, hours){
        this._location = location;
        this._days = days;
        this._hours = hours;
    }
    get location(){
        return this._location;
    }
    get days(){
        return this._days;
    }
    get hours(){
        return this._hours;
    }
    set location(newLocation){
        this._location = newLocation;
    }
    set days(newDays){
        this._days = newDays;
    }
    set hours(newHours){
        this._hours = newHours;
    }
    callPackWithoutLackAPI(){
        // Instantiate the Shell object and invoke its execute method.
        const response = await fetch('http://example.com/movies.json');
        console.log(response);
        
    }
    deconstructOutput(){
        const BoulderJudgement = output['BoulderJudgement'];
        //Colour Tags: G OKGREEN, L OKLIGHTBLUE, B BLUE, W WARNING, F FAIL, R REDUNDERBLACK
        let colour = BoulderJudgement.match(/[GLBWFR]/); //Matches first letter of boulder judgement (colour tag)
        let judgement = BoulderJudgement.match(/[GLBWFR]#(.*)/); //Matched Everything after # (Boulder judgement)
        return colour, judgement
    }
}
function callFunction(){
    location = 'EH£9jN';
    days = '2';
    hours ='6';
    // Instantiate the Shell object and invoke its execute method.
    const execSync = require('child_process').execSync;
    call = 'python PackWithoutLack.py ' + location + ' ' +  days + ' ' + hour;
    output = execSync(call, { encoding: 'utf-8' }); 
    document.write(console.log(output));
}
*/
function returnPack(){
    for (let clothes in ClothesDict){
        if(ClothesDict[clothes] === 'True'){
            document.write(clothes + '\t');
        }
    }
}
function returnLack(){
    for (let clothes in ClothesDict){
        if(ClothesDict[clothes] === 'False'){
            document.write(clothes +'\t');
        }
    }
}