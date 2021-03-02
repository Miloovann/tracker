/*let width;
const screenDetect = () =>{
    width = document.documentElement.clientWidth;
    if(width<1365){ //change width
        document.getElementById('navbar').style.display = 'none'; //foreword to award chunk
        document.getElementById('mnavbar').style.display = 'block'; //hamburger icon
    }
    else{
        document.getElementById('navbar').style.display = 'block';
        document.getElementById('mnavbar').style.display = 'none';
        closeside();
    }
}

const openside = () =>{
    document.getElementById('msidebar').style.width = '250px'; //actual sidebar when click hamburger
    document.querySelector('#mnavbar a').style.display = 'none';
}
const closeside = () =>{
    document.getElementById('msidebar').style.width = '0px';
    document.querySelector('#mnavbar a').style.display = 'block';
}

window.addEventListener("resize", screenDetect);

screenDetect();*/

var today = new Date();
var m = today.getMonth();
var d = today.getDate();
if(m===0){m = 'January';}
else if(m===1){m = 'February';}            
else if(m===2){m = 'March';}
else if(m===3){m = 'April';}
else if(m===4){m = 'May';}
else if(m===5){m = 'June';}
else if(m===6){m = 'July';}
else if(m===7){m = 'August';}
else if(m===8){m = 'September';}
else if(m===9){m = 'October';}
else if(m===10){m = 'November';}
else if(m===11){m = 'December';}

// start csv
$.get(m+d+"all.csv", function(data) {
    var build = '<table  cellpadding="2" cellspacing="0" style="border-collapse: collapse" width="80%">\n';
    var head = data.split("\n");
    for (var i = 0; i < 1; i++) {
        build += "<tr>";
        currentRow = head[i].split(",");
        for (let i2 = 0; i2 < currentRow.length; i2++) {
            build += `<th>${currentRow[i2]}</th>`;
        }
        build += "</tr>";
    }
    for (var i = 1; i < head.length; i++) {
        build += "<tr>";
        currentRow = head[i].split(",");
        if (currentRow.length === 8){
            for (let i2 = 0; i2 < currentRow.length; i2++) {
                build += `<td>${currentRow[i2]}</td>`;
            }
        }
        build += "</tr>";
    }
    build += "</table>";
    document.getElementById("inttable").innerHTML = build;
});

$.get(m+d+"africa"+"all.csv", function(data) {
    var build = '<table  cellpadding="2" cellspacing="0" style="border-collapse: collapse" width="80%">\n';
    var head = data.split("\n");
    for (var i = 0; i < 1; i++) {
        build += "<tr>";
        currentRow = head[i].split(",");
        for (let i2 = 0; i2 < currentRow.length; i2++) {
            build += `<th>${currentRow[i2]}</th>`;
        }
        build += "</tr>";
    }
    for (var i = 1; i < head.length; i++) {
        build += "<tr>";
        currentRow = head[i].split(",");
        if (currentRow.length === 8){
            for (let i2 = 0; i2 < currentRow.length; i2++) {
                build += `<td>${currentRow[i2]}</td>`;
            }
        }
        build += "</tr>";
    }
    build += "</table>";
    document.getElementById("afrtable").innerHTML = build;
});

$.get(m+d+"northamerica"+"all.csv", function(data) {
    var build = '<table  cellpadding="2" cellspacing="0" style="border-collapse: collapse" width="80%">\n';
    var head = data.split("\n");
    for (var i = 0; i < 1; i++) {
        build += "<tr>";
        currentRow = head[i].split(",");
        for (let i2 = 0; i2 < currentRow.length; i2++) {
            build += `<th>${currentRow[i2]}</th>`;
        }
        build += "</tr>";
    }
    for (var i = 1; i < head.length; i++) {
        build += "<tr>";
        currentRow = head[i].split(",");
        if (currentRow.length === 8){
            for (let i2 = 0; i2 < currentRow.length; i2++) {
                build += `<td>${currentRow[i2]}</td>`;
            }
        }
        build += "</tr>";
    }
    build += "</table>";
    document.getElementById("namtable").innerHTML = build;
});

$.get(m+d+"southamerica"+"all.csv", function(data) {
    var build = '<table  cellpadding="2" cellspacing="0" style="border-collapse: collapse" width="80%">\n';
    var head = data.split("\n");
    for (var i = 0; i < 1; i++) {
        build += "<tr>";
        currentRow = head[i].split(",");
        for (let i2 = 0; i2 < currentRow.length; i2++) {
            build += `<th>${currentRow[i2]}</th>`;
        }
        build += "</tr>";
    }
    for (var i = 1; i < head.length; i++) {
        build += "<tr>";
        currentRow = head[i].split(",");
        if (currentRow.length === 8){
            for (let i2 = 0; i2 < currentRow.length; i2++) {
                build += `<td>${currentRow[i2]}</td>`;
            }
        }
        build += "</tr>";
    }
    build += "</table>";
    document.getElementById("samtable").innerHTML = build;
});

$.get(m+d+"asia"+"all.csv", function(data) {
    var build = '<table  cellpadding="2" cellspacing="0" style="border-collapse: collapse" width="80%">\n';
    var head = data.split("\n");
    for (var i = 0; i < 1; i++) {
        build += "<tr>";
        currentRow = head[i].split(",");
        for (let i2 = 0; i2 < currentRow.length; i2++) {
            build += `<th>${currentRow[i2]}</th>`;
        }
        build += "</tr>";
    }
    for (var i = 1; i < head.length; i++) {
        build += "<tr>";
        currentRow = head[i].split(",");
        if (currentRow.length === 8){
            for (let i2 = 0; i2 < currentRow.length; i2++) {
                build += `<td>${currentRow[i2]}</td>`;
            }
        }
        build += "</tr>";
    }
    build += "</table>";
    document.getElementById("asatable").innerHTML = build;
});

$.get(m+d+"AustraliaOceania"+"all.csv", function(data) {
    var build = '<table  cellpadding="2" cellspacing="0" style="border-collapse: collapse" width="80%">\n';
    var head = data.split("\n");
    for (var i = 0; i < 1; i++) {
        build += "<tr>";
        currentRow = head[i].split(",");
        for (let i2 = 0; i2 < currentRow.length; i2++) {
            build += `<th>${currentRow[i2]}</th>`;
        }
        build += "</tr>";
    }
    for (var i = 1; i < head.length; i++) {
        build += "<tr>";
        currentRow = head[i].split(",");
        if (currentRow.length === 8){
            for (let i2 = 0; i2 < currentRow.length; i2++) {
                build += `<td>${currentRow[i2]}</td>`;
            }
        }
        build += "</tr>";
    }
    build += "</table>";
    document.getElementById("austable").innerHTML = build;
});

$.get(m+d+"europe"+"all.csv", function(data) {
    var build = '<table  cellpadding="2" cellspacing="0" style="border-collapse: collapse" width="80%">\n';
    var head = data.split("\n");
    for (var i = 0; i < 1; i++) {
        build += "<tr>";
        currentRow = head[i].split(",");
        for (let i2 = 0; i2 < currentRow.length; i2++) {
            build += `<th>${currentRow[i2]}</th>`;
        }
        build += "</tr>";
    }
    for (var i = 1; i < head.length; i++) {
        build += "<tr>";
        currentRow = head[i].split(",");
        if (currentRow.length === 8){
            for (let i2 = 0; i2 < currentRow.length; i2++) {
                build += `<td>${currentRow[i2]}</td>`;
            }
        }
        build += "</tr>";
    }
    build += "</table>";
    document.getElementById("eutable").innerHTML = build;
});
// end csv

//Start Right Bar collection
$(document).ready(function(){
    $.ajax({
        type: "GET",
        url: m+d+"all.csv",
        dataType: "text",
        success: function(data) {processData(data);}
    });
});
var lines = [];
function processData(allText) {
var allTextLines = allText.split(/\r\n|\n/);
var headers = allTextLines[0].split(',');
var i=218;
var data = allTextLines[i].split(',');
if (data.length == headers.length) {
    var tarr = [];
    for (var j=0; j<headers.length; j++) {
        tarr.push(headers[j]);
        tarr.push(data[j]);
    }
    lines.push(tarr);
}
function lengthof(a){
    for (var k=0; k<10000; k++){
        if(a[k] === undefined){
            return k;
            break;
        }
    }
}
function splitstring(a){
    var s = "";
    q = lengthof(a);
    special = q%3;
    counter = 0;
    for (var j=0; j<q; j++){
    if (counter >= special){
    if ((j-special)%3===0&&j!==0){
        s += ",";
    }
    }
        s+=a[j];
    counter +=1;
    }
    return s;
}
document.getElementById('total_cases').innerHTML = splitstring(lines[0][3]);
document.getElementById('total_deaths').innerHTML = splitstring(lines[0][7]);
document.getElementById('total_recovered').innerHTML = splitstring(lines[0][11]);
}
//End Right Bar Collection

//Start Filter Function to automatically set a initial page 
function filter(a){
    inter = document.getElementsByClassName('int');
    singapore = document.getElementsByClassName('singapore');
    eu = document.getElementsByClassName('eu');
    asa = document.getElementsByClassName('asa');
    aus = document.getElementsByClassName('aus');
    afr = document.getElementsByClassName('afr');
    nam = document.getElementsByClassName('nam');
    sam = document.getElementsByClassName('sam');
    for(var i=0; i<inter.length; i++)       {inter[i].style.display = 'none';}
    for(var i=0; i<singapore.length;i++)    {singapore[i].style.display = 'none';}
    for(var i=0; i<eu.length; i++)          {eu[i].style.display = 'none';}
    for(var i=0; i<asa.length; i++)         {asa[i].style.display = 'none';}
    for(var i=0; i<aus.length; i++)         {aus[i].style.display = 'none';}
    for(var i=0; i<afr.length; i++)         {afr[i].style.display = 'none';}
    for(var i=0; i<nam.length; i++)         {nam[i].style.display = 'none';}
    for(var i=0; i<sam.length; i++)         {sam[i].style.display = 'none';}
    b = document.getElementsByClassName(a);
    for(var i=0; i<b.length; i++)       {b[i].style.display = 'inline-block';}
}
//End Filter Function 1.0

//Start Filter Function to set auto sg graph
function sgfilter(a){
    minus0 = document.getElementById('minus0').style.display = 'none';
    minus1 = document.getElementById('minus1').style.display = 'none';
    minus2 = document.getElementById('minus2').style.display = 'none';
    minus3 = document.getElementById('minus3').style.display = 'none';
    minus4 = document.getElementById('minus4').style.display = 'none';
    minus5 = document.getElementById('minus5').style.display = 'none';
    minus6 = document.getElementById('minus6').style.display = 'none';
    minus7 = document.getElementById('minus7').style.display = 'none';
    minus8 = document.getElementById('minus8').style.display = 'none';
    minus9 = document.getElementById('minus9').style.display = 'none';
    minus10 = document.getElementById('minus10').style.display = 'none';
    minus11 = document.getElementById('minus11').style.display = 'none';
    minus12 = document.getElementById('minus12').style.display = 'none';
    minus13 = document.getElementById('minus13').style.display = 'none';
    b = document.getElementById(a).style.display = 'inline-block';
}
//End Filter Function 2.0

//Start Comm Filter Function
function communityfilter(a){
    communitybarsg = document.getElementById('communitybarsg').style.display = 'none';
    communitylinesg = document.getElementById('communitylinesg').style.display = 'none';
    b = document.getElementById(a).style.display = 'inline-block';
}
//End Filter Functiom Comm

//Start dorm Filter Function
function dormfilter(a){
    dormbarsg = document.getElementById('dormbarsg').style.display = 'none';
    dormlinesg = document.getElementById('dormlinesg').style.display = 'none';
    b = document.getElementById(a).style.display = 'inline-block';
}
//End Filter Function dorm

//Start total Filter Function
function totalfilter(a){
    totalbarsg = document.getElementById('totalbarsg').style.display = 'none';
    totallinesg = document.getElementById('totallinesg').style.display = 'none';
    b = document.getElementById(a).style.display = 'inline-block';
}
//End Filter Function total

//Start imported Filter Function
function importedfilter(a){
    importedbarsg = document.getElementById('importedbarsg').style.display = 'none';
    importedlinesg = document.getElementById('importedlinesg').style.display = 'none';
    b = document.getElementById(a).style.display = 'inline-block';
}
//End Filter Function imported

function timeFunc(){
    fetch('/updatetiming.txt')
        .then(response => response.text())
        .then(data => {
            console.log(data)
            var units = " second"
            var upd = data.split(" ");
            var prev = new Date(upd[0],upd[1],upd[2],upd[3],upd[4],upd[5]);
            var a = new Date();
            var now = new Date(a.getFullYear(), a.getMonth()+1, a.getDate(), a.getHours(), a.getMinutes(), a.getSeconds());
            var time = (now - prev)/1000;
            if (time > 1 && time < 60) units = " seconds"
            else if (time >= 60){
                remain = time % 60
                time -= remain
                time/=60
                units=" minute"
                if (time > 1 && time < 60) units = " minutes"
                else if (time >= 60){
                    remain = time % 60
                    time -= remain
                    time/=60
                    units=" hour"
                    if (time > 1 && time < 24) units = " hours"
                    else if (time >= 24){
                        remain = time % 24
                        time -= remain
                        time/=24
                        units=" day"
                        if (time > 1 && time < 7) units = " days"
                        else if (time >= 7){
                            remain = time % 7
                            time -= remain
                            time/=7
                            units=" week"
                            if (time > 1) units = " weeks"
                        }
                    }
                }
            }
            document.getElementById("timedif").innerHTML = "Updated: " + time + units + " ago";
        });
}
timeFunc()