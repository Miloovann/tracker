var abbrev = [['int', 'worldwide'],['afr', 'africa'],['asa', 'asia'],['aus', 'AustraliaOceania'],['eu', 'europe'],['nam', 'north America'], ['sam', 'south America']];
var graphtype = ['total', 'death', 'recovered'];
var continentsdata = '';
abbrev.forEach(cont=>{
    continentsdata += '<div class="' + cont[0] + '" style="padding-top: 130px;">';
    graphtype.forEach(type=>{
        continentsdata += '<img src = "' + cont[1] + type + '10.svg" style="width: 26%;">';
    });
    continentsdata += '<div class="table-responsive" id = "' + cont[0] + 'table"></div><p>*If data is consistent across all sources, reliability = 1. If data is taken only from Worldometers, reliability = 0</p></div>';
});

var localsgdata = '<div class="singapore" style="padding-top: 130px;">';

sgvirus = [['total', 'All Cases'], ['community', 'Community'], ['imported', 'Imported'], ['dorm', 'Dormitory']];
charttype = ['Bar', 'Line'];

sgvirus.forEach(sgcase=>{
    localsgdata += '<div><br><div class="dropdown' + sgcase[0] + '"><button class="dropbtn' + sgcase[0] + '">' + sgcase[1] + ' Graphs</button><div class="dropdown' + sgcase[0] + '-content">';
    charttype.forEach(chart=>{
        localsgdata += '<p class="hover" onclick="' + sgcase[0] + 'filter(\'' + sgcase[0] + chart.toLowerCase() + 'sg\')" style="font-size:16px">' + chart + '</p>';
    });
    localsgdata += '</div></div>';
    charttype.forEach(chart=>{
        localsgdata += '<img id = "' + sgcase[0] + chart.toLowerCase() + 'sg" src="SG' + sgcase[0] + chart.toLowerCase() + '14D.svg" style="width:40%">';
    });
    localsgdata += '</div>';
});
localsgdata += '<div><br><div class="dropdownsgall"><button class="dropbtnsgall">Date</button><div class="dropdownsgall-content">';
for(var iter=0; iter<14; iter++){
    localsgdata += '<p class="hover" id = "label' + iter + '" onclick="sgfilter(\'minus' + iter + '\')" style="font-size:16px"></p>' //innerHTML is weeks[iter]
}
localsgdata += '</div></div>';

for(var i=0; i<14; i++) localsgdata += '<img id = "minus'+ i + '">'; //double quotation may have error
localsgdata += '</div></div>';

continentsdata += localsgdata;
document.getElementById('Global').innerHTML = continentsdata;

const checkfileexists = (url) =>{
    var http = new XMLHttpRequest(); 
    http.open('HEAD', url, false); 
    http.send(); 
    if (http.status === 200)    return true;
    else    return false;
}

function sgdatelink(){
    var fortnight = [];
    for(var days=0; days<=14; days++){
        var date = new Date();
        var last = new Date(date.getTime() - (days * 24 * 60 * 60 * 1000));
        var day =last.getDate();
        var month=last.getMonth();
        if(month===0){month = 'Jan';}
        else if(month===1){month = 'Feb';}            
        else if(month===2){month = 'Mar';}
        else if(month===3){month = 'Apr';}
        else if(month===4){month = 'May';}
        else if(month===5){month = 'Jun';}
        else if(month===6){month = 'Jul';}
        else if(month===7){month = 'Aug';}
        else if(month===8){month = 'Sep';}
        else if(month===9){month = 'Oct';}
        else if(month===10){month = 'Nov';}
        else if(month===11){month = 'Dec';}

        date = day+' '+month;
        filename = 'http://127.0.0.1:5500/'; //rmb change url
        filename += 'SG\ ' + day+'\ '+month + '\ Cases.svg';
        console.log(filename);
        if(checkfileexists(filename)){
            console.log("exists");
            fortnight.push(date)
            document.getElementById('minus'+days).setAttribute('src', filename);
            document.getElementById('label'+days).innerHTML = date;
        }
    }
}
sgdatelink();