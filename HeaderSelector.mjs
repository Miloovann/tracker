var continents = [['int', 'Global'],['singapore', 'Singapore'],['afr', 'Africa'],['asa', 'Asia'],['aus', 'Oceania'],['eu', 'Europe'],['nam', 'N. America'], ['sam', 'S. America']];
var filterfunctioncode = '';
continents.forEach(cont=>{
    filterfunctioncode += '<li class="nav-item"><p class="hover nav-item nav-link" onclick="filter(\'' + cont[0] + '\')" style="font-size:25px; color:white">' + cont[1] + '</p></li>';
});
document.getElementById("international_hover").innerHTML = filterfunctioncode;