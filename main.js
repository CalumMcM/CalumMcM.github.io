

function callPackWithoutLack(locationGIVEN, daysGIVEN, hoursGIVEN){
    var xhttp = new XMLHttpRequest();
    console.log(locationGIVEN + "HELLO");
    xhttp.open("GET", "http://127.0.0.1:5000/main/"+locationGIVEN+"/"+daysGIVEN+"/"+hoursGIVEN, true);
    xhttp.send();
    xhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        ClothesDict = (this.responseText);
        console.log(ClothesDict);
        returnBoulderJudgement(ClothesDict);
        returnClothes('True', 1, 'InvisConLeft');
        returnClothes('True', 0, 'InvisConRight');
        returnClothes('False', 1, 'InvisConLeft');
        returnClothes('False', 0);
      }
    };
}
function returnBoulderJudgement(ClothesDictUNJ){
    ClothesDict = JSON.parse(ClothesDictUNJ)
    console.log(ClothesDict);
    boulderJudgementFull = ClothesDict['BoulderJudgement'];
    console.log(boulderJudgementFull);
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
    } else {
        document.getElementById('BoulderResultsContainerRight').innerHTML = "<span style='color:"+colour+"'>"+judgement[0]+"</span>";
        console.log(judgement[0]);
    }
}
function returnClothes(Truth, divider){
    /*
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
    */
}
function returnSummary(){
    document.getElementById('SummaryContainerRight').innerHTML = ClothesDict['summary'];
    loadDoc();
}
function loadDoc() {
    
  }
  //https://api.opencagedata.com/geocode/v1/json?q=EH39JN&key=b71199c8872647f888aee90d767ae10b