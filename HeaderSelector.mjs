var continents = [['int', 'World'],['singapore', 'Singapore'],['afr', 'Africa'],['asa', 'Asia'],['aus', 'Oceania'],['eu', 'Europe'],['nam', 'N. America'], ['sam', 'S. America']];
var filterfunctioncode = '';
continents.forEach(cont=>{
    filterfunctioncode += '<li class="nav-item"><a class="hover nav-item nav-link" onclick="filter(\'' + cont[0] + '\')" style="font-size:25px; color:white"  data-toggle="collapse" data-target=".navbar-collapse.show">' + cont[1] + '</a></li>';
});
document.getElementById("international_hover").innerHTML += filterfunctioncode;
