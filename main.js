class APICall{
    constructor(location, days, hours, output){
        this._location = location;
        this._days = days;
        this._hours = hours;
        this._output = output;
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
    get output(){
        return this._output;
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
        const execSync = require('child_process').execSync;
        call = 'python PackWithoutLack.py ' + this._location + ' ' +  this._days + ' ' + this._hours
        const output = execSync(call, { encoding: 'utf-8' }); 
        this._output = output; //Setter for output
    }
    deconstructOutput(){
        const BoulderJudgement = this._output['BoulderJudgement'];
        //Colour Tags: G OKGREEN, L OKLIGHTBLUE, B BLUE, W WARNING, F FAIL, R REDUNDERBLACK
        let colour = BoulderJudgement.match(/[GLBWFR]/); //Matches first letter of boulder judgement (colour tag)
        let judgement = BoulderJudgement.match(/[GLBWFR]#(.*)/); //Matched Everything after # (Boulder judgement)
        return colour, judgement
    }
}
