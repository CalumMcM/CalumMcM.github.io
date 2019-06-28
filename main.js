
ClothesDict = {'summary':"Highest amount of rainfall on a given day will be  0.4mm on Tuesday.<br>Highest temperature will be 19\u00b0C on Wednesday. <br>Lowest temperature will be 5\u00b0C on Tuesday.",'BoulderJudgement':'Blue|Very wet and cold','Street Shoes':'True', 'Gloves':'False','Wellies':'False','Street Trousers':'True','Waterproof Jacket':'False','Jumper':'False','Sunglasses':'False','Duvet Jacket':'False','Waterproof Jacket':'False','Suncream Facter 30':'False','Suncream Facter 50':'False','T-shirt':'True','Wooly hat':'False','Thermals':'False'};

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
    Clothes.ClothesDict = execSync(call, { encoding: 'utf-8' }); 
    document.write(console.log(output));
}
*/
function returnBoulderJudgement(){
    boulderJudgementFull = ClothesDict['BoulderJudgement'];
    //Colour Tags: G OKGREEN, L OKLIGHTBLUE, B BLUE, W WARNING, F FAIL, R REDUNDERBLACK
    let colour = boulderJudgementFull.match(/Green|skyblue|Blue|Warning|89243A|Red/); //Matches first letter of boulder judgement (colour tag)
    let judgement = boulderJudgementFull.match(/[^\|]*$/); //Matched Everything after # (Boulder judgement)
    if (colour[0] == 'Warning'){
        document.getElementById('BoulderResultsContainerRight').style.backgroundColor = "yellow";
        document.write(judgement[0].fontcolor('black').fontsize(5).bold());
    } 
    else if (colour[0] == 'Red'){
        document.getElementById('BoulderResultsContainerRight').style.backgroundColor = "Red";
        document.write(judgement[0].fontcolor('white').fontsize(5).bold());
    } else {
        document.write(judgement[0].fontcolor(colour[0]).fontsize(5).bold());
    }

}
function returnClothes(Truth, divider){
    let iterator = 1;
    for (let clothes in ClothesDict){
        if(ClothesDict[clothes] === Truth){
            if ((iterator%2)==divider){
                if (Truth == 'True'){
                    document.write(' + ' + clothes +'<br> ');
                } else{
                    document.write(' - ' + clothes +'<br> ');
                }
            }
            iterator++;
        }
    }
}
function returnSummary(){
    document.getElementById('SummaryContainerRight').innerHTML = ClothesDict['summary'];
}