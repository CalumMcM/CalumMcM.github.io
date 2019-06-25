/*
function callPackWithoutLackAPI(location, days, hours){
    
}
var exec = require('child_process').exec, child;
*/
// Instantiate the Shell object and invoke its execute method.
const execSync = require('child_process').execSync;
// import { execSync } from 'child_process';  // replace ^ if using ES modules
call = 'python PackWithoutLack.py' + ' EH39JN ' + '5 ' + '40'
const output = execSync(call, { encoding: 'utf-8' });  // the default is 'buffer'
console.log(output);