import requests, csv, json, math, os, datetime, http.client, io, logging
import pandas as pd, sys, urllib3, numpy as np, matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from operator import itemgetter
from telethon import TelegramClient

with open("/Users/junyiho/Desktop/Scripts/Archive/CovidHunter/updatetiming.txt", 'w') as f:
	f.write(datetime.datetime.now().strftime("%-Y %-m %-d %-H %-M %-S"))