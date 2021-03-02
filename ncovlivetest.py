import requests, csv, json, math, os, datetime, http.client, io, logging
import pandas as pd, sys, tabula, urllib3, numpy as np, matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from operator import itemgetter
from telethon import TelegramClient
from tabula import read_pdf,convert_into
plt.rcParams.update({'figure.max_open_warning': 0})
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logging.getLogger().setLevel(logging.CRITICAL)

dir_name = "/Users/junyiho/Desktop/PW_Web"
test = os.listdir(dir_name)

for item in test:
    if item.endswith(".csv") or item.endswith(".svg"):
        os.remove(os.path.join(dir_name, item))

head = ["Country","Total Cases","New Cases","Total Deaths","New Deaths","Total Recovered","Continent","Reliability*"]
trackernames, worldonames, ncovnames = [],[],[]
ncovwrong = ["The Bahamas", "The Gambia","United Arab Emirates",
           "United Kingdom","United States","Curacao","Cape Verde",
           "SÃ£o TomÃ© and PrÃ\xadncipe","Reunion","Turks and Caicos Islands","TOTAL"]

ncovright = ["Bahamas","Gambia","UAE","UK","USA","Curaçao",
           "Cabo Verde","São Tomé and Príncipe","Réunion","Turks and Caicos","World"]

ncovempty = ['Congo', 'Kosovo', 'Sint Maarten', 'World']

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
        checker = msg.find(" new Covid-19 cases were announced earlier today (")
        if msg.count("Total") == 3 and msg.find("VIRUS UPDATE: ") == 0 and checker != -1:
            dd = int(msg.find(month + '. ')+len(month)+2)
            if msg[dd+1].isnumeric() is True:   messageday = msg[dd:dd+2]
            else:   messageday = msg[dd:dd+1]
            
            sgdischarged = int(countnumbers(msg,"Total discharged: ",18))
            sgdeaths = int(countnumbers(msg,"Total deaths: ",14))
            return [sgdeaths, sgdischarged, messageday == date_num]

async def yesterday():      ##to check new deaths
    async for message in client.iter_messages(-1001123464890):
        msg = str(message.raw_text)
        checker = msg.find(" new Covid-19 cases were announced earlier today (")
        if msg.count("Total") == 3 and msg.find("VIRUS UPDATE: ") == 0 and checker != -1:
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
        with open('/Users/junyiho/Desktop/MOH.csv', 'r+') as f:
            for i in reversed(list(csv.reader(f))):
                    date = i[0]
                    if date != othercases[0]: #update local grouped data if not updated in csv yet
                        with open('/Users/junyiho/Desktop/MOH.csv', 'a') as f:
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

    with open("/Users/junyiho/Desktop/PW_Web/" + "SGCovid.csv","w",newline = '') as f:
        sglog = sgdata[0:6] + [month + " " + date_num]
        csv.writer(f).writerow(sglog)
#End mothership scraping

#Scrape NCOV2019.live
url = 'https://ncov2019.live/data/world'
src = requests.get(url).text
soup = BeautifulSoup(src,'lxml')
table = soup.find('table',id="sortable_table_world")
content = table.find('tbody').find_all('tr')
with open("/Users/junyiho/Desktop/PW_Web/" + 'livencov.csv','w',newline='',encoding='utf-8')as f:
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