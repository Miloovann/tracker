import requests, csv, json, math, os, datetime, http.client, io, logging
import pandas as pd, sys, urllib3, numpy as np, matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from operator import itemgetter
from telethon import TelegramClient
plt.rcParams.update({'figure.max_open_warning': 0})
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logging.getLogger().setLevel(logging.CRITICAL)

filedate = datetime.datetime.now().strftime("%B") + str(datetime.datetime.now().day)
countrynames = ["Africa","Worldwide","Asia","AustraliaOceania","Europe", "North America","South America"]
csvfilenames = ["africaall.csv","all.csv","asiaall.csv","australiaoceaniaall.csv","europeall.csv", "northamericaall.csv","southamericaall.csv"]

plt.rcParams.update({'font.family':'sans-serif'})
plt.rcParams.update({'font.sans-serif':'Verdana'})

##Graphing function for horizontal bar graphs
def graphbarh(colnum, casetype, casesave):
    for x in range(len(csvfilenames)):
        with open("/Users/junyiho/Desktop/Scripts/Archive/CovidHunter/" + csvfilenames[x], 'r') as f:
            data, world = [],[]
            for row in list(csv.reader(f)):
                if row[0] != "Country" and row[0] != "World":
                    if len(row[colnum]) != 0:
                        if row[colnum] != "N/A" and row[colnum].isdigit() == True:    data.append([row[0],int(row[colnum])])
                    else:   data.append([row[0],0])
                elif row[0] == "World":    world = [row[0],int(row[colnum])/1000000]
        data.sort(key = itemgetter(1), reverse = True)
        hightotal, highall = plt.subplots()
        if x == 3:
            y_axis, barwidth = [data[i][0] for i in range(len(data))], [data[i][1] for i in range(len(data))]
            specialtitle = "%s countries with most "+ casetype +" in Australia/Oceania"
            highall.set_title(specialtitle %len(y_axis), fontweight='bold') ##Australia has ~10 countries
        else:
            y_axis, barwidth = [data[i][0] for i in range(10)], [data[i][1] for i in range(10)]
            if x == 1:  highall.set_title("10 countries with most " + casetype + " " + countrynames[x], fontweight='bold') ##worldwide
            else:   highall.set_title("10 countries with most " + casetype+ " in " + countrynames[x], fontweight='bold') ##rest of the continents

        if len(str(barwidth[0])) >= 7:
            highall.set_xlabel("Total " + casetype + " in millions")
            barwidth = [i/1000000 for i in barwidth]
        else:   highall.set_xlabel("Total " + casetype)
        highall.barh(y_axis, barwidth)
        highall.set_yticks(highall.get_yticks())
        highall.set_yticklabels(y_axis, fontsize = 10, rotation = 45)
        highall.set_xlim(xmin=0)
        hightotal.savefig("/Users/junyiho/Desktop/Scripts/Archive/CovidHunter/" + countrynames[x] + casesave, format='svg', bbox_inches='tight', transparent=True)

graphbarh(1, "cases", "total10.svg")
graphbarh(3, "deaths", "death10.svg")
graphbarh(5, "recovered cases", "recovered10.svg")
##End Global Graphs

##Start Singapore Graphs
dates, imported, community, dorm, total = [],[],[],[],[]
with open('/Users/junyiho/Desktop/Scripts/Archive/CovidHunter/MOH.csv', 'r') as f:
    loop = 0
    for row in reversed(list(csv.reader(f))):
        if len(row) == 0:   continue
        loop += 1
        dates.append(row[0])
        imported.append(int(row[1])) 
        community.append(int(row[2]))
        dorm.append(int(row[3]))
        total.append(int(row[4]))
        if loop == 14:   break
dates, imported, community, dorm, total = dates[::-1], imported[::-1], community[::-1], dorm[::-1], total[::-1]
y_pos = np.arange(len(dates))

##Bar Line graphs 14 days
linefigures = [[total,'SG Total Cases over the past 14 days', 'SGtotalline14D.svg'],
 [imported, 'SG Imported Cases over the past 14 days', 'SGimportedline14D.svg'],
 [community, 'SG Community Cases over the past 14 days', 'SGcommunityline14D.svg'],
 [dorm, 'SG Dormitory Cases over the past 14 days', 'SGdormline14D.svg']]

barfigures = [[total, 'SG Total Cases over the past 14 days', 'SGtotalbar14D.svg'],
 [imported, 'SG Imported Cases over the past 14 days', 'SGimportedbar14D.svg'],
 [community, 'SG Community Cases over the past 14 days', 'SGcommunitybar14D.svg'],
 [dorm, 'SG Dormitory Cases over the past 14 days', "SGdormbar14D.svg"]]

def singaporegraphs(ynumb, titlename, figurename):
    ALLSG, SG = plt.subplots()
    SG.plot(dates, ynumb)
    SG.set_title(titlename, fontweight='bold')
    SG.set_xticks(SG.get_xticks())
    SG.set_xticklabels(dates, rotation=45)
    SG.set_ylim(ymin=0)
    ALLSG.savefig("/Users/junyiho/Desktop/Scripts/Archive/CovidHunter/" + figurename, format='svg', bbox_inches='tight', transparent=True)

def singaporebargraphs(ynumb,titlename,figurename):
    ALLSG, SG = plt.subplots()
    SG.bar(dates, ynumb)
    SG.set_title(titlename, fontweight='bold')
    SG.set_xticks(SG.get_xticks())
    SG.set_xticklabels(dates, rotation=45)
    SG.set_ylim(ymin=0)
    ALLSG.savefig("/Users/junyiho/Desktop/Scripts/Archive/CovidHunter/" + figurename, format='svg', bbox_inches='tight', transparent=True)

for i in linefigures:
    singaporegraphs(i[0],i[1],i[2])

for i in barfigures:
    singaporebargraphs(i[0],i[1],i[2])

##Pie Charts latest distribution of cases
for i in range(len(total)):
          circle, chart = plt.subplots()
          day = [dorm[i], community[i], imported[i]]

          x, y, colors = np.array(['Dorm', 'Community', 'Imported']), np.array(day), ['xkcd:lavender', 'maroon', 'turquoise']
          percent = 100*y/y.sum()
          patches, texts = plt.pie(y, colors=colors, startangle=90, radius=1.2)
          labels = ['{0} -- {1:1.2f}% -- {2} Cases'.format(i,j,k) for i,j,k in zip(x, percent, y)]
          
          lgn = chart.legend(patches, labels, bbox_to_anchor=(-0.1, 1.), fontsize=10)
          lgn.set_title(dates[i] + " Total -- "+ str(total[i])+" Cases")
          chart.set_title("SG " + dates[i] + " Cases", fontweight='bold')
          circle.savefig("/Users/junyiho/Desktop/Scripts/Archive/CovidHunter/" + "SG " + dates[i] + " Cases.svg", format = "svg", bbox_inches='tight', transparent=True)
##End Singapore Graphs

with open("/Users/junyiho/Desktop/Scripts/Archive/CovidHunter/updatetiming.txt", 'w') as f:
	f.write(datetime.datetime.now().strftime("%-Y %-m %-d %-H %-M %-S"))
