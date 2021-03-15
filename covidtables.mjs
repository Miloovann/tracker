var abbrev = [['int', 'worldwide'],['afr', 'africa'],['asa', 'asia'],['aus', 'AustraliaOceania'],['eu', 'europe'],['nam', 'north America'], ['sam', 'south America']];
var graphtype = ['total', 'death', 'recovered'];
var continentsdata = '';
abbrev.forEach(cont=>{
    continentsdata += '<div class="' + cont[0] + '" style="padding: 130px 40px 0px 20px;">';
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

for(var i=0; i<14; i++) localsgdata += '<img id = "minus'+ i + '">';
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
function sgdatelink(days, boole){
    var date = new Date();
    var last = new Date(date.getTime() - (days * 24 * 60 * 60 * 1000));
    var day =last.getDate();
    var month=last.toLocaleString("default", {month: 'short'});

    date = day+' '+month;
    filename = 'https://covidhunter.netlify.app/'; //rmb change url
    filename += 'SG\ ' + day+'\ '+month + '\ Cases.svg';
    var check = checkfileexists(filename);
    if(check){
        if(boole) days--;
        document.getElementById('minus'+days).setAttribute('src', filename);
        document.getElementById('label'+days).innerHTML = date;
    }
    return check;
}
var countbackDays=0;
var minus = false;
var limit = 13;
while(countbackDays <= limit){
    var run = sgdatelink(countbackDays, minus);
    if(!run){
        minus = true;
        limit = 14;
    }
    countbackDays++;
}