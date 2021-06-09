import requests, csv, json, math, os, datetime, http.client, io, logging
import pandas as pd, sys, tabula, urllib3, numpy as np, matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from operator import itemgetter
from telethon import TelegramClient
from tabula import read_pdf,convert_into
plt.rcParams.update({'figure.max_open_warning': 0})
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logging.getLogger().setLevel(logging.CRITICAL)

dir_name = "/Users/junyiho/Desktop/Scripts/PW_Web"
test = os.listdir(dir_name)

for item in test:
    if (item.endswith(".csv") or item.endswith(".svg")) and item != "MOH.csv":
        os.remove(os.path.join(dir_name, item))

head = ["Country","Total Cases","New Cases","Total Deaths","New Deaths","Total Recovered","Continent","Reliability*"]
trackernames, worldonames, ncovnames = [],[],[]
ncovwrong = ["The Bahamas", "The Gambia","United Arab Emirates",
           "United Kingdom","United States","Curacao","Cape Verde",
           "SÃ£o TomÃ© and PrÃ\xadncipe","Reunion","Turks and Caicos Islands","TOTAL"]

ncovright = ["Bahamas","Gambia","UAE","UK","USA","Curaçao",
           "Cabo Verde","São Tomé and Príncipe","Réunion","Turks and Caicos","World"]

ncovempty = ['Congo', 'Kosovo', 'Sint Maarten', 'World', 'Kiribati']

worldowrong=["S. Korea","DRC","CAR","St. Barth",
             "St. Vincent Grenadines","Saint Pierre Miquelon",
             "Faeroe Islands","Sao Tome and Principe"]

worldoright=["South Korea","DR Congo","Central African Republic",
             "Saint Barthelemy","Saint Vincent and the Grenadines",
             "Saint Pierre and Miquelon","Faroe Islands",
             "São Tomé and Príncipe"]

worldoempty = ['Africa', 'Asia', 'Congo', 'Europe', 'North America', 'Oceania',
               'Sint Maarten', 'South America', 'World','Diamond Princess', 'MS Zaandam']

trackerwrong = ["DRC","CAR","Sao Tome and Principe",
                "Faeroe Islands","St. Barth","S. Korea","St. Vincent Grenadines",
                "Saint Pierre Miquelon"]

trackerright = ["DR Congo","Central African Republic","São Tomé and Príncipe","Faroe Islands",
                "Saint Barthelemy","South Korea","Saint Vincent and the Grenadines",
                "Saint Pierre and Miquelon"]

trackerempty = ['Brunei ',"United Arab Emirates","Côte d'Ivoire","Guernsey","Jersey", 'MS Zaandam', ##not in web
                'Guam','Kosovo','Puerto Rico','U.S. Virgin Islands','Diamond Princess'] ##in web but cannot compare

trackerrepeat = ["Central African Republic","Faroe Islands","Saint Vincent and the Grenadines"]
repeatbool = [False,False,False]

##Start all data collection and cleaning
#Start mothership scraping
api_id, api_hash = 1239249, '9bc7bce40bfb10c3eabfaf220b77a0a0'
client = TelegramClient('tester', api_id, api_hash)

month = datetime.datetime.now().strftime("%b") ##today's month
date_num = str(datetime.datetime.now().day)
mothership_afternoon_key = "[JUST IN] Covid-19 update in S'pore on "

def getnum(msg, casetype):
    C = msg.find(casetype) + len(casetype)
    msg = msg[C: len(msg)]
    case = ""
    for i in range(len(msg)):
            if msg[i+1].isnumeric() == False and msg[i].isnumeric() == False:   break
            else:   case += msg[i]
    case = case.replace(",","")
    return case

async def afternoon():
    async for message in client.iter_messages(-1001123464890):
        msg = str(message.raw_text)
        position = msg.find(mothership_afternoon_key)
        if position == 0: ##if message is virus update
            casetype = ["* Imported cases: ", "* Community cases: ", "* Dorm cases: ","NEW CASES: ", "Total cases: "]
            varcase = ["impo", "comm", "dorm", 'new', "total"]
            datadict = {}
            for i in range(5):
                datadict["{}".format(varcase[i])] = getnum(msg, casetype[i])
            dd = int(msg.find(month + '. ')+len(month)+2)
            if msg[dd+1].isnumeric() is True:   messageday = msg[dd:dd+2]
            else:   messageday = msg[dd:dd+1]

            return list(datadict.values()) + [messageday == date_num] #["impo", "comm", "dorm", 'new', "total", msgday == tdy]

def countnumbers(text, title, siz):
    posi = text.find(title) + siz
    string = ""
    while text[posi].isdigit() or text[posi] == ",":
        if text[posi].isdigit(): string += text[posi]
        posi += 1
        if posi == len(text):   break
    return string

async def night():
    async for message in client.iter_messages(-1001123464890):
        msg = str(message.raw_text)
        # checker = msg.find(" new Covid-19 cases were announced earlier today (")
        if msg.count("Total") == 3 and msg.find("VIRUS UPDATE: ") == 0:
            dd = int(msg.find(month + '. ')+len(month)+2)
            if msg[dd+1].isnumeric() is True:   messageday = msg[dd:dd+2]
            else:   messageday = msg[dd:dd+1]
            
            sgdischarged = int(countnumbers(msg,"Total discharged: ",18))
            sgdeaths = int(countnumbers(msg,"Total deaths: ",14))
            return [sgdeaths, sgdischarged, messageday == date_num]

async def yesterday():      ##to check new deaths
    async for message in client.iter_messages(-1001123464890):
        msg = str(message.raw_text)
        # checker = msg.find(" new Covid-19 cases were announced earlier today (")
        if msg.count("Total") == 3 and msg.find("VIRUS UPDATE: ") == 0:
            dd = int(msg.find(month + '. ')+len(month)+2)
            if msg[dd+1].isnumeric() is True:   messageday = msg[dd:dd+2]
            else:   messageday = msg[dd:dd+1]

            if messageday != date_num:
                    sgdeaths = int(countnumbers(msg,"Total deaths: ",14))
                    return sgdeaths
with client:
    ##if today's both msg not out, take yest's totalcases,totaldeaths,totalrecovery, newcases and newdeaths reset become ""
    ##if only morning msg out, take today's totalcases and newcases, totaldeaths and totalrecovery take yest's, newdeaths reset become ""
    ##if both out, take everything from today

    work = client.loop.run_until_complete(afternoon())
    if work[5]: ##update local grouped data if latest mothership afternoon data is from today
        othercases = list([date_num + " "  + month] + work[0:4])
        with open('/Users/junyiho/Desktop/Scripts/PW_Web/MOH.csv', 'r+') as f:
            for i in reversed(list(csv.reader(f))):
                    date = i[0]
                    if date != othercases[0]: #update local grouped data if not updated in csv yet
                        with open('/Users/junyiho/Desktop/Scripts/PW_Web/MOH.csv', 'a') as f:
                                f.write('\n')
                                writer = csv.writer(f)
                                writer.writerow(othercases)
                    break
        
        work = [work[4],work[3]]
    else:   work = [work[4], ""]

    sleep = client.loop.run_until_complete(night())
    if sleep[2] == True: ##if latest release from mothership is today
            ystd = client.loop.run_until_complete(yesterday())
            if sleep[0] != ystd:    newdeaths = sleep[0] - ystd
            else:   newdeaths = ""
    else:   newdeaths = ""
    sleep.insert(1,newdeaths)
    sgdata = ["Singapore"]+work+sleep[0:3]+["Asia"]

# with open("/Users/junyiho/Desktop/Scripts/PW_Web/" + "SGCovid.csv","w",newline = '') as f:
#     sglog = sgdata[0:6] + [month + " " + date_num]
#     csv.writer(f).writerow(sglog)
#End mothership scraping

#Scrape NCOV2019.live
url = 'https://ncov2019.live/data/world'
src = requests.get(url).text
soup = BeautifulSoup(src,'lxml')
table = soup.find('table',id="sortable_table_world")
content = table.find('tbody').find_all('tr')
with open("/Users/junyiho/Desktop/Scripts/PW_Web/" + 'livencov.csv','w',newline='',encoding='utf-8')as f:
    writer = csv.writer(f)
    csvrow=["Country,Other","TotalCases","NewCases","NewCases%","TotalDeaths","NewDeaths","NewDeaths%","TotalRecovered"]
    for row in content:
        csvrow = []
        check = -1 #remove unnecessary columns, "critical" and "active"
        emptybuffer = False
        for a in row.find_all('td'):
            check += 1
            if check in [0,1,3,7]:
                buffer = a.text.strip()
                if(check==0):
                    if(buffer[0]=="★"): buffer = buffer[1:len(buffer)].strip()
                    if buffer in ncovwrong: buffer = ncovright[ncovwrong.index(buffer)]
                    if buffer in ncovempty:
                        emptybuffer = True
                        break
                    ncovnames.append(buffer)
                elif buffer == "Unknown": buffer = "N/A"
                elif buffer == '0':   buffer = ''
                buffer = buffer.replace(",","")

                if check==7 and buffer.find("+")!=-1:
                    buffer = buffer[0:buffer.find("+")]
                    
                crazyvar = ''
                if check==1 or check==3:
                    plus = buffer.find("+")
                    if plus != -1:
                        crazyvar = buffer[plus+1:]
                        buffer = buffer[0:plus]
                    csvrow += [buffer,crazyvar]
                else:
                    csvrow += [buffer]
        if emptybuffer ==  False:
            if csvrow[0] == "Singapore":
                writer.writerow(sgdata[0:6])
            else:
                writer.writerow(csvrow)
f.close()
#End Scrape NCOV2019.live

#Scrape Worldometers
url = 'https://www.worldometers.info/coronavirus/'
source = requests.get(url).text
soup = BeautifulSoup(source,'lxml')
table = soup.find('table',id="main_table_countries_today")
with open("/Users/junyiho/Desktop/Scripts/PW_Web/" + 'metersworld.csv','w',newline='')as f:
    writer = csv.writer(f)
    for row in table.find_all('tr'):
        csvRow = []
        check = -1 #remove unnecessary columns that we dont want
        rowedit = False # remove rows if empty or starting with 'total'
        print("\n\n\n")
        for data in row.find_all('td'):
            print(data)
            buffer=data.text.strip()
            if rowedit == True or buffer == 'Total:' or (buffer == '' and check == 0):# last condition is to remove rows that have an empty first column
                rowedit = True
            else:
                check+=1
                if (check == 1): ##check=1 means country name
                    if buffer in worldoempty: buffer = ""
                    elif buffer in worldowrong:
                        buffer = worldoright[worldowrong.index(buffer)]
                    if len(buffer)!=0:  worldonames.append(buffer)
                   
                if (check > 0 and check < 7) or check == len(row.find_all('td')):
                    buffer = buffer.replace(",","")
                    if len(buffer) > 0 and buffer[0] != "+":    csvRow.append(buffer)
                    else:   csvRow.append(buffer[1:len(buffer)])
        if rowedit == False and [line.split(',')[0] for line in csvRow] != [] and len(csvRow[0]) != 0:
            if csvRow[0] == "Singapore":    writer.writerow(sgdata)
            else:
                writer.writerow(csvRow)
f.close()
#End Scrape Worldometers

# #Scrape Corona Tracker
# r=requests.get("https://api.coronatracker.com/v3/stats/worldometer/topCountry")
# result = r.json()
# with open("/Users/junyiho/Desktop/Scripts/PW_Web/" + 'tracker.csv','w',newline='')as f:
#     writer = csv.writer(f)
#     scrape = ["country","totalConfirmed","totalDeaths","totalRecovered","dailyConfirmed","dailyDeaths"]
#     for x in result:
#         csvrow = []
#         for y in x:
#             if y in scrape:
#                 csvrow.append('') if x[y] == 0 else csvrow.append(x[y])
           
#         if csvrow[0] in trackerwrong:   csvrow[0] = trackerright[trackerwrong.index(csvrow[0])]
#         elif csvrow[0] in trackerempty:   continue
#         if csvrow[0] in trackerrepeat:
#             if repeatbool[trackerrepeat.index(csvrow[0])] == True:  continue
#             else: repeatbool[trackerrepeat.index(csvrow[0])] = True
#         csvrow[2],csvrow[4] = csvrow[4],csvrow[2]
#         csvrow[3],csvrow[4] = csvrow[4],csvrow[3]
#         csvrow[5],csvrow[4] = csvrow[4],csvrow[5]
#         if csvrow[0] == "Singapore":    writer.writerow(sgdata[0:6])
#         else:   writer.writerow(csvrow)
#         trackernames.append(csvrow[0])
# f.close()
# #End Scrape Corona Tracker
# ##End all data collection and cleaning

# #Print extra variables if any
# def diff(a,b,c):
#     if [x for x in a if x not in b] != []:  print("NCOV2019live extra, not found in Worldometers: \n",      [x for x in a if x not in b])
#     if [x for x in a if x not in c] != []:  print("NCOV2019live extra, not found in Corona Tracker: \n",    [x for x in a if x not in c])
#     if [x for x in b if x not in a] != []:  print("\nWorldometers extra, not found in NCOV2019live: \n",    [x for x in b if x not in a])
#     if [x for x in b if x not in c] != []:  print("Worldometers extra, not found in Corona Tracker: \n",    [x for x in b if x not in c])
#     if [x for x in c if x not in a] != []:  print("\nCorona Trackers extra, not found in NCOV2019live: \n", [x for x in c if x not in a])
#     if [x for x in c if x not in b] != []:  print("Corona Trackers extra, not found in Worldometers: \n",   [x for x in c if x not in b])

# diff(sorted(ncovnames),sorted(worldonames),sorted(trackernames))

# #sorting country names alphabetically
# def sortcountries(csvname):
#     with open(csvname, 'r') as f:   data = [line for line in csv.reader(f)]
#     data.sort(key=itemgetter(0))
#     with open(csvname, 'w+') as f:  csv.writer(f).writerows(data)

# sortcountries("/Users/junyiho/Desktop/Scripts/PW_Web/tracker.csv")
# sortcountries("/Users/junyiho/Desktop/Scripts/PW_Web/livencov.csv")
# sortcountries("/Users/junyiho/Desktop/Scripts/PW_Web/metersworld.csv")
# #End sorting of country names

# #adding function
# def combinefinals(total,addition):
#     addition = str(addition)
#     total = str(total)
#     if len(addition) != 0 and len(total) != 0 and total.isdigit() == True and addition.isdigit() == True:
#         return (int(total) + int(addition))
#     else:   return total

# #start combining tracker,meters and livencov into 1 csv
# filedate = datetime.datetime.now().strftime("%B") + str(datetime.datetime.now().day)
# check = worldtotalcases = worldnewcases = worldtotaldeaths = worldnewdeaths = worldtotalrecovery = 0
# with open("/Users/junyiho/Desktop/Scripts/PW_Web/" + filedate + "all.csv","w",newline = '')as final:
#     w = csv.writer(final)
#     w.writerow(head)
#     with open("/Users/junyiho/Desktop/Scripts/PW_Web/livencov.csv","r",newline='')as fone:
#         readerone = list(csv.reader(fone))
#         with open("/Users/junyiho/Desktop/Scripts/PW_Web/tracker.csv","r",newline='')as ftwo:
#             readertwo = list(csv.reader(ftwo))
#             with open("/Users/junyiho/Desktop/Scripts/PW_Web/metersworld.csv","r",newline='')as fthree:
#                 readerthree = list(csv.reader(fthree))
#                 while check < len(readertwo):
#                     first = readerone[check]
#                     second = readertwo[check]
#                     third = readerthree[check]
                        
#                     if second == third[0:6] == first:   third.append(1)
#                     else:   third.append(0)
#                     third = [int(third[i]) if type(third[i]) == str and third[i].isdigit() else third[i] for i in range(len(third))]
#                     w.writerow(third)

#                     worldtotalcases = combinefinals(worldtotalcases,third[1])
#                     worldnewcases = combinefinals(worldnewcases,third[2])
#                     worldtotaldeaths = combinefinals(worldtotaldeaths,third[3])
#                     worldnewdeaths = combinefinals(worldnewdeaths,third[4])
#                     worldtotalrecovery = combinefinals(worldtotalrecovery,third[5])

#                     check += 1
#                 w.writerow(["World",worldtotalcases,worldnewcases,worldtotaldeaths,worldnewdeaths,worldtotalrecovery,"",0])
#             fthree.close()
#         ftwo.close()
#     fone.close()
# final.close()
# # for i in ["/Users/junyiho/Desktop/Scripts/PW_Web/metersworld.csv","/Users/junyiho/Desktop/Scripts/PW_Web/livencov.csv","/Users/junyiho/Desktop/Scripts/PW_Web/tracker.csv"]:    os.remove(i)
# #End Combining tracker,meters and livencov into 1 csv

# #Start analysis of all.csv
# ###Start Logarithm analysis of all data
# ##with open("/Users/junyiho/Desktop/Scripts/PW_Web/" + filedate + "logall.csv","w",newline='')as flog:
# ##    writer = csv.writer(flog)
# ##    with open("/Users/junyiho/Desktop/Scripts/PW_Web/" + filedate + "all.csv",'r')as foriginal:
# ##        reader = list(csv.reader(foriginal))
# ##        for row in reader:
# ##            logrow = []
# ##            for i in range(len(row)):
# ##                if row[i].isnumeric() and i != len(row)-1:
# ##                    print(row, i)
# ##                    logrow.append(math.log10(int(row[i])))  ##need int(i) because isnumeric doesnt mean is in int format
# ##                else:
# ##                    logrow.append(row[i])
# ##            writer.writerow(logrow)
# ###End Logarithm analysis of all data

# #Start splitting function of data into continents
# def SortSplitContinents(csvname):
#     f = open("/Users/junyiho/Desktop/Scripts/PW_Web/" + filedate + csvname, 'r')
#     data = [line for line in csv.reader(f)]
#     data.sort(key=itemgetter(6))
#     names = ["africa","asia","australiaoceania","europe","northamerica","southamerica"]
#     cont = names.copy()
#     for i in range(len(names)):
#         names[i] = open("/Users/junyiho/Desktop/Scripts/PW_Web/" + filedate + names[i] + csvname, 'w+')
#         csv.writer(names[i]).writerow(head)
#     for i in range(len(data)):
#         dataname = data[i][6].replace(" ","").replace("/","").lower()
#         if dataname in cont:    csv.writer(names[cont.index(dataname)]).writerow(data[i])

# SortSplitContinents("all.csv")
# #SortSplitContinents("logall.csv")
# #End splitting function of data into continents

# ##Start Global Graphs
# filedate = datetime.datetime.now().strftime("%B") + str(datetime.datetime.now().day)
# csvfilenames = ["africaall.csv","all.csv","asiaall.csv","australiaoceaniaall.csv","europeall.csv", "northamericaall.csv","southamericaall.csv"]
# countrynames = ["Africa","Worldwide","Asia","AustraliaOceania","Europe", "North America","South America"]

# ##Graphing function for horizontal bar graphs
# def graphbarh(colnum, casetype, casesave):
#     for x in range(len(csvfilenames)):
#         with open("/Users/junyiho/Desktop/Scripts/PW_Web/" + filedate + csvfilenames[x], 'r') as f:
#             data, world = [],[]
#             for row in list(csv.reader(f)):
#                 if row[0] != "Country" and row[0] != "World":
#                     if len(row[colnum]) != 0:
#                         if row[colnum] != "N/A":    data.append([row[0],int(row[colnum])])
#                     else:   data.append([row[0],0])
#                 elif row[0] == "World":    world = [row[0],int(row[colnum])/1000000]
#         data.sort(key = itemgetter(1), reverse = True)
#         hightotal, highall = plt.subplots()
#         if x == 3:
#             x_axis, y_axis = [data[i][0] for i in range(len(data))], [data[i][1] for i in range(len(data))]
#             specialtitle = "%s countries with most "+ casetype +" in Australia/Oceania"
#             highall.set_title(specialtitle %len(x_axis), fontweight='bold') ##Australia has ~10 countries
#         else:
#             print(data)
#             x_axis, y_axis = [data[i][0] for i in range(10)], [data[i][1] for i in range(10)]
#             if x == 1:  highall.set_title("10 countries with most " + casetype + " " + countrynames[x], fontweight='bold') ##worldwide
#             else:   highall.set_title("10 countries with most " + casetype+ " in " + countrynames[x], fontweight='bold') ##rest of the continents

#         if len(str(y_axis[0])) >= 7:
#             highall.set_xlabel("Total " + casetype + " in millions")
#             y_axis = [i/1000000 for i in y_axis]
#         else:   highall.set_xlabel("Total " + casetype)
#         highall.barh(x_axis, y_axis)
#         highall.set_yticklabels(x_axis, fontsize = 10, rotation = 45)
#         highall.set_xlim(xmin=0)
#         hightotal.savefig("/Users/junyiho/Desktop/Scripts/PW_Web/" + countrynames[x] + casesave, format='svg', bbox_inches='tight', transparent=True)

# graphbarh(1, "cases", "total10.svg")
# graphbarh(3, "deaths", "death10.svg")
# graphbarh(5, "recovered cases", "recovered10.svg")
# ##End Global Graphs

# ##Start Singapore Graphs
# dates, imported, community, dorm, total = [],[],[],[],[]
# with open('/Users/junyiho/Desktop/Scripts/PW_Web/MOH.csv', 'r') as f:
#     loop = 0
#     for row in reversed(list(csv.reader(f))):
#         if len(row) == 0:   continue
#         loop += 1
#         dates.append(row[0])
#         imported.append(int(row[1])) 
#         community.append(int(row[2]))
#         dorm.append(int(row[3]))
#         total.append(int(row[4]))
#         if loop == 14:   break
# dates, imported, community, dorm, total = dates[::-1], imported[::-1], community[::-1], dorm[::-1], total[::-1]
# y_pos = np.arange(len(dates))

# ##Bar Line graphs 14 days
# linefigures = [[total,'SG Total Cases over the past 14 days', 'SGtotalline14D.svg'],
#  [imported, 'SG Imported Cases over the past 14 days', 'SGimportedline14D.svg'],
#  [community, 'SG Community Cases over the past 14 days', 'SGcommunityline14D.svg'],
#  [dorm, 'SG Dormitory Cases over the past 14 days', 'SGdormline14D.svg']]

# barfigures = [[total, 'SG Total Cases over the past 14 days', 'SGtotalbar14D.svg'],
#  [imported, 'SG Imported Cases over the past 14 days', 'SGimportedbar14D.svg'],
#  [community, 'SG Community Cases over the past 14 days', 'SGcommunitybar14D.svg'],
#  [dorm, 'SG Dormitory Cases over the past 14 days', "SGdormbar14D.svg"]]

# def singaporegraphs(ynumb, titlename, figurename):
#     ALLSG, SG = plt.subplots()
#     SG.plot(dates, ynumb)
#     SG.set_title(titlename, fontweight='bold')
#     SG.set_xticklabels(dates, rotation=45)
#     SG.set_ylim(ymin=0)
#     ALLSG.savefig("/Users/junyiho/Desktop/Scripts/PW_Web/" + figurename, format='svg', bbox_inches='tight', transparent=True)

# def singaporebargraphs(ynumb,titlename,figurename):
#     ALLSG, SG = plt.subplots()
#     SG.bar(dates, ynumb)
#     SG.set_title(titlename, fontweight='bold')
#     SG.set_xticklabels(dates, rotation=45)
#     SG.set_ylim(ymin=0)
#     ALLSG.savefig("/Users/junyiho/Desktop/Scripts/PW_Web/" + figurename, format='svg', bbox_inches='tight', transparent=True)

# for i in linefigures:
#     singaporegraphs(i[0],i[1],i[2])

# for i in barfigures:
#     singaporebargraphs(i[0],i[1],i[2])

# ##Pie Charts latest distribution of cases
# for i in range(len(total)):
#           circle, chart = plt.subplots()
#           day = [dorm[i], community[i], imported[i]]

#           x, y, colors = np.array(['Dorm', 'Community', 'Imported']), np.array(day), ['xkcd:lavender', 'maroon', 'turquoise']
#           percent = 100*y/y.sum()
#           patches, texts = plt.pie(y, colors=colors, startangle=90, radius=1.2)
#           labels = ['{0} -- {1:1.2f}% -- {2} Cases'.format(i,j,k) for i,j,k in zip(x, percent, y)]
          
#           lgn = chart.legend(patches, labels, bbox_to_anchor=(-0.1, 1.), fontsize=10)
#           lgn.set_title(dates[i] + " Total -- "+ str(total[i])+" Cases")
#           chart.set_title("SG " + dates[i] + " Cases", fontweight='bold')
#           circle.savefig("/Users/junyiho/Desktop/Scripts/PW_Web/" + "SG " + dates[i] + " Cases.svg", format = "svg", bbox_inches='tight', transparent=True)
# ##End Singapore Graphs

# with open("/Users/junyiho/Desktop/Scripts/PW_Web/updatetiming.txt", 'w') as f:
# 	f.write(datetime.datetime.now().strftime("%-Y %-m %-d %-H %-M %-S"))