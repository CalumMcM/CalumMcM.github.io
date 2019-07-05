

function callPackWithoutLack(locationGIVEN, daysGIVEN, hoursGIVEN){
    var xhttp = new XMLHttpRequest();
    locationGIVEN = locationGIVEN.replace(/\s/g, '');
    if (hoursGIVEN == ""){
        hoursGIVEN = daysGIVEN * 24;
    }
    xhttp.open("GET", "https://thebravesttoaster.pythonanywhere.com/main/"+locationGIVEN+"/"+daysGIVEN+"/"+hoursGIVEN, true);
    console.log("<Powered By Dark Sky>");
    xhttp.send();
    xhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        ClothesDict = (this.responseText);
        returnBoulderJudgement(ClothesDict, daysGIVEN);
        returnClothes('True', 1, 'InvisConLeft1', ClothesDict);
        returnClothes('True', 0, 'InvisConRight1', ClothesDict);
        if (daysGIVEN < 3){
            
        }
        else {
            returnForecast(ClothesDict);
        }
        
        returnSummary(ClothesDict);
      }
    };
}
function returnBoulderJudgement(ClothesDictUNJ, daysGIVEN){
    ClothesDict = JSON.parse(ClothesDictUNJ)
    boulderJudgementFull = ClothesDict['BoulderJudgement'];
    if ( daysGIVEN < 3){
        //Colour Tags: G OKGREEN, L OKLIGHTBLUE, B BLUE, W WARNING, F FAIL, R REDUNDERBLACK
        let colour = boulderJudgementFull.match(/Green|skyblue|Blue|Warning|89243A|Red/); //Matches first letter of boulder judgement (colour tag)
		let judgement = boulderJudgementFull.match(/[^\|]*$/); //Matched Everything after # (Boulder judgement)
		console.log(boulderJudgementFull);
		if (colour[0] == 'Warning') {
			document.getElementById('BoulderResultsContainerRight').style.backgroundColor = "yellow";
			document.getElementById('BoulderResultsContainerRight').innerHTML = "<span style='color:black'>&#9888" + judgement[0] + "&#9888</span>";
		}
		else if (colour[0] == 'Red') {
			document.getElementById('BoulderResultsContainerRight').style.backgroundColor = "Red";
			document.getElementById('BoulderResultsContainerRight').innerHTML = "<span style='color:white'>&#10060" + judgement[0] + "&#10060</span>";
		}
		else if (colour[0] == 'Blue') {
			document.getElementById('BoulderResultsContainerRight').innerHTML = "<span style='color:" + colour[0] + "'>&#127783" + judgement[0] + "&#127783</span>";
		}
		else if (colour[0] == 'skyblue') {
			document.getElementById('BoulderResultsContainerRight').innerHTML = "<span style='color:" + colour[0] + "'>&#x1F4A7" + judgement[0] + "&#x1F4A7</span>";
		}
		else if (colour[0] == '89243A') {
			document.getElementById('BoulderResultsContainerRight').innerHTML = "<span style='color:#8B0000'>&#128721" + judgement[0] + "&#128721</span>";
		}
		else if (colour[0] == 'Green') {
			document.getElementById('BoulderResultsContainerRight').innerHTML = "<span style='color:" + colour[0] + "'>&#10004" + judgement[0] + "&#10004</span>";
		}
		else {
			document.getElementById('BoulderResultsContainerRight').innerHTML = "<span style='color:HotPink; font-size: 20px'>&#9762Unkown judgement Recieved. Proceed with caution.&#9762</span>";
		}
    } 
    else {
        document.getElementById('BoulderResultsContainerLeft').innerHTML = "<span style='font-family: Simplifica;font-size: 22.5px; line-height: 20px'><center> <h3> Boulderable Days </h3></center></span>";
        //for (let boulderAbleDay in boulderJudgementFull)
        if (boulderJudgementFull == "Absolutely none of them"){
            document.getElementById('BoulderResultsContainerRight').innerHTML += "<span style='color:Red;font-size: 22.5px'>" + boulderJudgementFull + "</span>";
        } else{
            document.getElementById('BoulderResultsContainerRight').innerHTML += "<span style='color:Green;font-size: 22.5px'>" + boulderJudgementFull + "</span>";
        }
    }
    
}
function returnClothes(Truth, divider, container, ClothesDict){
    let iterator = 1;
    for (let clothes in ClothesDict){
        if(ClothesDict[clothes] === Truth){
            if ((iterator%2)==divider){ //Divider means every second item from the list is printed to the page
                if (Truth == 'True'){
                    document.getElementById(container).innerHTML += clothes +'<br> ' ;
                } else{
                    document.getElementById(container).innerHTML += clothes +'<br> ' ;
                }
            }
            iterator++;
        }
    }
}
function returnForecast(ClothesDict){
    document.getElementById('ResultBotContainer').style.display = 'block';
    document.getElementById('LackBreakLine').style.display = 'block';
    document.getElementById('ResultBotContainer').innerHTML = '<center><span style="color: black;line-height:0px;"><h2>Forecast</h2></span></center>'
    document.getElementById('forecastContainer0').innerHTML = '<span style="color: black;"><u>Day</u></span><br><br>'
    document.getElementById('forecastContainer1').innerHTML = '<center><span style="color: black;"><u>Highest Rainfall In An Hour(mm)</u></span><br><br></center>'
    document.getElementById('forecastContainer2').innerHTML = '<span style="color: black;"><u>Highest Apparent Temperature (C)</u></span><br>'
    document.getElementById('forecastContainer3').innerHTML = '<span style="color: black;"><u>Lowest Apparent Temperature (C)</u></span><br>'
    document.getElementById('forecastContainer4').innerHTML = '<span style="color: black;"><u>Cloud Cover (%)</u></span><br><br>'
    forecast = ClothesDict['forecast']
    for (let i = 0; i<forecast['days'].length;i++){
        if (i%2==0){
            colorPrint = 'grey'
        } else {
            colorPrint = 'black'
        }
        document.getElementById('forecastContainer0').innerHTML += '<span style="color: '+colorPrint+';">' + forecast['days'][i] + '</span><br>'
        document.getElementById('forecastContainer1').innerHTML += '<span style="color: '+colorPrint+';">' + forecast['rains'][i] + '</span><br>'
        document.getElementById('forecastContainer2').innerHTML += '<span style="color: '+colorPrint+';">' + forecast['tempMaxs'][i] + '</span><br>'
        document.getElementById('forecastContainer3').innerHTML += '<span style="color: '+colorPrint+';">' + forecast['tempMins'][i] + '</span><br>'
        document.getElementById('forecastContainer4').innerHTML += '<span style="color: '+colorPrint+';">' + forecast['cloudCovers'][i] + '</span><br>'

    }
    //document.getElementById('InvisibleContainerForecast').innerHTML = '<p style="color: black; font-family: courier"><br>Powered By DarkSky</p>'

}
function returnSummary(ClothesDict){
    document.getElementById('SummaryContainer').innerHTML ="<span style='font-size:20px;'>"+ClothesDict['summary']+"</span>";
}

  //https://api.opencagedata.com/geocode/v1/json?q=EH39JN&key=b71199c8872647f888aee90d767ae10b
