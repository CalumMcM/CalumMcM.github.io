
builder 

getter 

setter 


function callPackWithoutLackAPI(location, days, hours){
    // Instantiate the Shell object and invoke its execute method.
    const execSync = require('child_process').execSync;
    // import { execSync } from 'child_process'; 
    call = 'python PackWithoutLack.py ' + location + ' ' +  days + ' ' + hours
    const output = execSync(call, { encoding: 'utf-8' });  // the default is 'buffer'
    console.log(output);
}
callPackWithoutLackAPI('EH39JN', '2', '4')