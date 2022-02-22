import json
with open("./Covidapi.json", "r") as f:
    x = json.loads(f.read())
    
with open("./continent.json", "r") as g:
    y = json.loads(g.read())

new = {}

noa = {}
soa = {}
oce = {}
eur = {}
asi = {}
afr = {}

continents = []

for i in range(len(x)):
    del x[i]["countryCode"]
    del x[i]["country"]
    del x[i]["lat"]
    del x[i]["lng"]
    del x[i]["FR"]
    del x[i]["PR"]
    del x[i]["lastUpdated"]
    del x[i]["activeCases"]
    del x[i]["totalConfirmedPerMillionPopulation"]
    del x[i]["totalDeathsPerMillionPopulation"]
    country = x[i]["countryName"]
    del x[i]["countryName"]
    del x[i]["totalCritical"]
    new[country] = x[i]


for i in new:
    try:
        new[i] = new[i] | y[i]
        continents.append(y[i]['Continent'])
        if new[i]['Continent'] == "North America":
            noa[i] = new[i]
        elif new[i]['Continent'] == "South America":
            soa[i] = new[i]
        elif new[i]['Continent'] == "Africa":
            afr[i] = new[i]
        elif new[i]['Continent'] == "Asia":
            asi[i] = new[i]
        elif new[i]['Continent'] == "Europe":
            eur[i] = new[i]
        elif new[i]['Continent'] == "Oceania":
            oce[i] = new[i]
            
    except:
        pass
    

with open("./northamericaall.json", "w") as h:
    h.write(json.dumps(noa))

with open("./southamericaall.json", "w") as h:
    h.write(json.dumps(soa))

with open("./australiaoceaniaall.json", "w") as h:
    h.write(json.dumps(oce))
    
with open("./asiaall.json", "w") as h:
    h.write(json.dumps(asi))

with open("./africaall.json", "w") as h:
    h.write(json.dumps(afr))

with open("./europeall.json", "w") as h:
    h.write(json.dumps(eur))


with open("./all.json", "w") as h:
    h.write(json.dumps(new))

