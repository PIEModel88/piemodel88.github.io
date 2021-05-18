#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 15 20:43:34 2021

@author: ivamn
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 11 14:51:17 2021

@author: ivamn
"""



import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import sys
import os
import urllib.request
import csv
import re
import io
from github import Github
from datetime import datetime
import pytz
# pretty-print python data structures
from pprint import pprint
  
# for parsing all the tables present 
# on the website
from html_table_parser import HTMLTableParser
  
# for converting the parsed data in a
# pandas dataframe
import pandas as pd
import numpy as np
from sys import exit

from datetime import timedelta 
from datetime import datetime

from selenium.webdriver.chrome.options import Options
options = Options()
options.add_argument("--enable-javascript")
options.add_argument('--headless')
options.add_argument('--disable-gpu')  # Last I checked this was necessary.
driver = webdriver.Chrome('./chromedriver', chrome_options=options)

date_format = "%d/%m/%Y"

tz_HK = pytz.timezone('Asia/Hong_Kong') 
  
race_yr = '2021'
race_month = '05'
race_day = '19'
race_venue = 'HV'
race_start = '1'
race_nos = '9'

static_time = datetime.now(tz_HK).strftime("%Y/%m/%d, %H:%M:%S")
translation = {39: None} 
static_time_second = datetime.now(tz_HK).timestamp()
pool_table = []  

#Pass the race number from the calling script
# race_start = int(sys.argv[1])
# if len(sys.argv) > 2:
#     race_nos = sys.argv[2]
# else:
#     race_nos = race_start
for x in range(int(race_start), int(race_nos)+1):
    #url of the page we want to scrape
    
    url = "https://bet.hkjc.com/racing/pages/odds_turnover.aspx?lang=ch&date=" + str(race_yr) + "-" + str(race_month) + "-" + \
        str(race_day) + "&venue=" + str(race_venue) + "&raceno=" + str(x) 
    
    driver.get(url) 
      
    # this is just to ensure that the page is loaded
    time.sleep(1) 
      
    html = driver.page_source
      
    # this renders the JS code and stores all
    # of the information in static HTML code.
      
    # Now, we could simply apply bs4 to html variable
    soup = BeautifulSoup(html, "html.parser")

    df = pd.DataFrame(soup)
    #print(soup.prettify())
    
    
    race_turnover_table = soup.find_all("table")
    for spn in race_turnover_table[0].find_all("span"):
        #print(str(spn.get('id')) + ' ' + spn.text)
        dic = {}
        dic['date'] = str(race_yr)+ str(race_month)+str(race_day)
        dic['race'] = x
        dic['turnover_pool'] = str(spn.get('id')).replace('\n', '').strip().translate(translation)
        dic['turnover'] = str(spn.text).replace('\n', '').strip().translate(translation)
        dic['timestamp'] = static_time
        pool_table.append(dic)    


pool_table_df = pd.DataFrame (pool_table)
try:
    with open('/Users/ivamn/Documents/horse/Test/pool_table.csv') as f:
        pool_table_csv = pd.read_csv (r'/Users/ivamn/Documents/horse/Test/pool_table.csv')
        merge_pool = [pool_table_df, pool_table_csv]  
        result_pool = pd.concat(merge_pool)
        result_pool.sort_values(by=['date', 'timestamp','race', 'turnover_pool'], ascending=[True, True, True, True], inplace=True)
        result_pool.to_csv(r'/Users/ivamn/Documents/horse/Test/pool_table.csv', index = False)
        f.close()   
except IOError:
    result_pool = pool_table_df.copy()
    result_pool.sort_values(by=['date', 'timestamp','race', 'turnover_pool'], ascending=[True, True, True, True], inplace=True)
    result_pool.to_csv(r'/Users/ivamn/Documents/horse/Test/pool_table.csv', index = False)