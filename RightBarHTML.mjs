coronatypes = ["Cases", "Deaths", "Recovered"];
rightbarcode = '';
coronatypes.forEach(element => {
    rightbarcode += '<hr><h3>Total ' + element + ': </h3><p id="total_' + element.toLowerCase() + '" style = "font-size:20px;"></p>';
});
rightbarcode += '<p id = "timedif" style="font-size: 20px"></p>';
document.getElementById("infection").innerHTML = rightbarcode;