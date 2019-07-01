

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
        returnClothes('True', 1, 'InvisConLeft1');
        returnClothes('True', 0, 'InvisConRight1');
        returnClothes('False', 1, 'InvisConLeft2');
        returnClothes('False', 0, 'InvisConRight2');
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
        if (colour[0] == 'Warning'){
            document.getElementById('BoulderResultsContainerRight').style.backgroundColor = "yellow";
            document.getElementById('BoulderResultsContainerRight').innerHTML = "<span style='color:black'>"+judgement[0]+"</span>";
        } 
        else if (colour[0] == 'Red'){
            document.getElementById('BoulderResultsContainerRight').style.backgroundColor = "Red";
            document.getElementById('BoulderResultsContainerRight').innerHTML = "<span style='color:white'>"+judgement[0]+"</span>";
        } 
        else {
            document.getElementById('BoulderResultsContainerRight').innerHTML = "<span style='color:"+colour+"'>"+judgement[0]+"</span>";
            console.log(judgement[0]);
        }
    } 
    else {
        document.getElementById('BoulderResultsContainerLeft').innerHTML = "<center> <h3> Boulderable Days </h3></center>";
        //for (let boulderAbleDay in boulderJudgementFull)
        document.getElementById('BoulderResultsContainerRight').innerHTML += "<span style='color:Green'>" + boulderJudgementFull + "</span>";
    }
    
}
function returnClothes(Truth, divider, container){
    let iterator = 1;
    for (let clothes in ClothesDict){
        if(ClothesDict[clothes] === Truth){
            if ((iterator%2)==divider){ //Divider means every second item from the list is printed to the page
                if (Truth == 'True'){
                    document.getElementById(container).innerHTML += ' + ' + clothes +'<br> ' ;
                } else{
                    document.getElementById(container).innerHTML += ' - ' + clothes +'<br> ' ;
                }
            }
            iterator++;
        }
    }
}
function returnSummary(ClothesDict){
    document.getElementById('SummaryContainerRight').innerHTML ="<span style='font-size:13px'>"+ClothesDict['summary']+"</span>";
}

  //https://api.opencagedata.com/geocode/v1/json?q=EH39JN&key=b71199c8872647f888aee90d767ae10b
