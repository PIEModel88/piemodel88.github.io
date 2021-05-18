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



date_format = "%d/%m/%Y"

tz_HK = pytz.timezone('Asia/Hong_Kong') 
  
race_start = sys.argv[1]
race_nos = sys.argv[2]
race_yr = sys.argv[3]
race_month = sys.argv[4]
race_day = sys.argv[5]
race_venue = sys.argv[6]
folder_path = sys.argv[7]

# race_yr = '2021'
# race_month = '05'
# race_day = '19'
# race_venue = 'HV'
# race_start = '1'
# race_nos = '1'

static_time = datetime.now(tz_HK).strftime("%Y/%m/%d, %H:%M:%S")
translation = {39: None} 
static_time_second = datetime.now(tz_HK).timestamp()

#PATH = "/Users/ivamn/Downloads/chromedriver.exe"
#driver = webdriver.Chrome('./chromedriver') 
from selenium.webdriver.chrome.options import Options
options = Options()
options.add_argument("--enable-javascript")
options.add_argument('--headless')
options.add_argument('--disable-gpu')  # Last I checked this was necessary.
driver = webdriver.Chrome('./chromedriver', chrome_options=options)

def fill_exceedances(x):
    count = 0
    prev_column = ''
    color_org = 'orange'
    color_red = 'red'
    color_green = 'green'  
    color_black = 'black'  
    df1 = pd.DataFrame('', index=x.index, columns=x.columns)
    table_boolean = x.copy()
    table_boolean_10 = x.copy()
    table_boolean_15 = x.copy()
    table_boolean_remove = x.copy()
    for column in x.columns:
  
        if count == 0:
            table_boolean [column] = True
            table_boolean_10 [column] = True
            table_boolean_15 [column] = True
            table_boolean_remove [column] = True
            prev_column = column
            count = 1
        else:
            if column[1] != prev_column[1] or column[2] != prev_column[2]:
                table_boolean [column] = True
                table_boolean_10 [column] = True
                table_boolean_15 [column] = True
                table_boolean_remove [column] = True
                prev_column = column
                count = 1                
            elif column[1] == prev_column[1] and column[2] == prev_column[2]:
                table_boolean [column] = (x[prev_column] - x[column])/x[prev_column] <= 0.05 
                table_boolean_10 [column] = (x[prev_column] - x[column])/x[prev_column] <= 0.1
                table_boolean_15 [column] = (x[prev_column] - x[column])/x[prev_column] <= 0.15  
                table_boolean_remove [column] = x[column] != -1
                prev_column = column
                count = count + 1
    
    #set color by mask and add missing non matched columns names by reindex
    df1 = (df1.where(table_boolean, 'background-color: {}'.format(color_green))
              .reindex(columns=x.columns, fill_value=''))
    df1 = (df1.where(table_boolean_10, 'background-color: {}'.format(color_org))
              .reindex(columns=x.columns, fill_value=''))
    df1 = (df1.where(table_boolean_15, 'background-color: {}'.format(color_red))
              .reindex(columns=x.columns, fill_value=''))
    df1 = (df1.where(table_boolean_remove, 'background-color: {}'.format(color_black))
              .reindex(columns=x.columns, fill_value=''))
    return df1

for x in range(int(race_start), int(race_nos)+1):
    #url of the page we want to scrape

    url = "https://bet.hkjc.com/racing/pages/odds_dbl.aspx?lang=ch&date=" + str(race_yr) + "-" + str(race_month) + "-" + \
        str(race_day) + "&venue=" + str(race_venue) + "&raceno=" + str(x) 


    
    race_table = []  
    driver.get(url) 
      
    # this is just to ensure that the page is loaded
    time.sleep(2) 
      
    html = driver.page_source
      
    # this renders the JS code and stores all
    # of the information in static HTML code.
      
    # Now, we could simply apply bs4 to html variable
    soup = BeautifulSoup(html, "html.parser")



    df = pd.DataFrame(soup)
    #print(soup.prettify())
    race_full_table = soup.find("div", attrs={"id": "dblTable"})
    row_count = 1
    dic = {}
    for tr in race_full_table.find_all("tr"):
        if row_count == 1:
            for td in tr.find_all('td'):
                True
            current_horse_count = td.text
            row_count = row_count + 1
        elif row_count ==2:
            for td in tr.find_all('td'):
                True
            next_horse_count = td.text
            row_count = row_count + 1
        else:
            for y in range(0, int(current_horse_count) + 1):
                dic = {}
                if y == 0:
                    next_horse_nos = tr.find_all('td')[0].text
                else:                    
                    dic['name'] = 'DBL'
                    dic['race'] = str(x).strip().translate(translation)
                    dic['current_race_horse'] = int(str(y).strip().translate(translation))
                    dic['next_race_horse'] = int(str(next_horse_nos).strip().translate(translation))

         
                    dic['timestamp'] = static_time
                    dic['timestamp_second'] = static_time_second
                    #print(tr.find_all('td')[y].text)
                    if tr.find_all('td')[y].text == '退出':
                        dic['odd'] = -1
                        race_table.append(dic)
                        
                    elif tr.find_all('td')[y].text != '':
                        dic['odd'] = float(tr.find_all('td')[y].text.replace('\n', '').strip().translate(translation))
                        race_table.append(dic)
                        
                    
            row_count = row_count + 1
  
#old double odd webpage
    # race_full_table = soup.find_all("td", attrs={"class": "tableNum2DBL"})
    
    # #Extract the odd value
    # for odd_row in race_full_table:
    #     f = io.StringIO()
    #     print(odd_row.find("a"), file=f)
    #     if str(f.getvalue()).find('(') !=  -1:                      
    #         a = f.getvalue().index('(')
    #         b = f.getvalue().index(')')
    #         dic = {}
    #         count = 0
    #         for sub in f.getvalue()[a+1:b].split(','):
    #             if count == 0:
    #                 dic['name'] = sub.replace('\n', '').strip().translate(translation)
    #                 count = count + 1
    #             elif count == 1:
    #                 dic['race'] = int(sub.replace('\n', '').strip().translate(translation))
    #                 count = count + 1
    #             elif count == 2:
    #                 dic['current_race_horse'] = int(sub.replace('\n', '').strip().translate(translation))
    #                 count = count + 1
    #             elif count == 3:
    #                 dic['next_race_horse'] = int(sub.replace('\n', '').strip().translate(translation))
    #                 count = count + 1
    #         dic['odd'] = float(odd_row.find("a").text.replace('\n', '').strip().translate(translation))
    #         dic['timestamp'] = static_time
    #         dic['timestamp_second'] = static_time_second
    #         race_table.append(dic)
            
    # race_full_table = soup.find_all("td", attrs={"class": "tableNum1DBL"})

    # #Extract the odd value
    # for odd_row in race_full_table:
    #     f = io.StringIO()
    #     print(odd_row.find("a"), file=f)
    #     if str(f.getvalue()).find('(') !=  -1:                      
    #         a = f.getvalue().index('(')
    #         b = f.getvalue().index(')')
    #         dic = {}
    #         count = 0
    #         for sub in f.getvalue()[a+1:b].split(','):
    #             if count == 0:
    #                 dic['name'] = sub.replace('\n', '').strip().translate(translation)
    #                 count = count + 1
    #             elif count == 1:
    #                 dic['race'] = int(sub.replace('\n', '').strip().translate(translation))
    #                 count = count + 1
    #             elif count == 2:
    #                 dic['current_race_horse'] = int(sub.replace('\n', '').strip().translate(translation))
    #                 count = count + 1
    #             elif count == 3:
    #                 dic['next_race_horse'] = int(sub.replace('\n', '').strip().translate(translation))
    #                 count = count + 1
    #         dic['odd'] = float(odd_row.find("a").text.replace('\n', '').strip().translate(translation))
    #         dic['timestamp'] = static_time
    #         race_table.append(dic)
#new double odd webpage     
     
    double_odd = pd.DataFrame (race_table)
    
    if double_odd.empty:
        print("No Odd Yet")
        exit()
        
    try:
        with open(folder_path + 'ext_double_odd_'+ str(x)  + '.csv') as f:
            hist_double_odd = pd.read_csv (folder_path + 'ext_double_odd_'+ str(x)  + '.csv')
            merge_odd = [double_odd, hist_double_odd]  
            result_odd = pd.concat(merge_odd)
            result_odd.sort_values(by=['timestamp','race', 'current_race_horse','next_race_horse'], ascending=[True, True, True, True], inplace=True)
            result_odd.to_csv(folder_path + 'ext_double_odd_' + str(x) + '.csv', index = False)
            f.close()
    except IOError:
        result_odd = double_odd.copy()
        result_odd.sort_values(by=['timestamp','race', 'current_race_horse','next_race_horse'], ascending=[True, True, True, True], inplace=True)
        result_odd.to_csv(folder_path + 'ext_double_odd_' + str(x) + '.csv', index = False)
   # arr = result_odd['timestamp_second'].unique()
   # sorted_array = arr[np.argsort(arr)][-20: ]
   # trim_table_temp = result_odd[result_odd['timestamp_second'].isin(sorted_array)]
    trim_table_temp = result_odd.copy()
    f=open(folder_path + 'double_odd_table' + str(x) + '.html','w')
    disable_cache1 = "<meta http-equiv=" + '"' + "Cache-Control" + '"' + " content=" + '"' + "no-cache, no-store, must-revalidate" + '"' + ">"
    disable_cache2 = "<meta http-equiv=" + '"' + "Pragma" + '"' + " content=" + '"' + "no-cache" + '"' + ">"
    disable_cache3 = "<meta http-equiv=" + '"' + "Expires" + '"' + " content=" + '"' + "0" + '"' + ">"
    f.write(disable_cache1)
    f.write(disable_cache2)
    f.write(disable_cache3)  
    page_refresh = "<meta content=" + '"' + "10" + '"' + " http-equiv=" + '"' + "refresh" + '"' + ">"
    f.write(page_refresh)
    f.write(static_time)
    url_link = "<A HREF=" + '"' + "../index.html" + '"' + ">Home            </A>"
    f.write(url_link)
    if x >=2:
        url_link = "<A HREF=" + '"' + "../page/double_odd_table" + str(int(x) - 1) + ".html" + '"' + ">Prev Race      " + str(int(x) - 1) + "</A>"
        f.write(url_link)            
    
    url_link = "<A HREF=" + '"' + "../page/double_odd_table" + str(int(x) + 1) + ".html" + '"' + ">Next Race          " + str(int(x) + 1) + "</A>"
    f.write(url_link)
    
    trim_table = trim_table_temp    
    table = pd.pivot_table(trim_table,index=['next_race_horse'],columns=['race','current_race_horse','timestamp'],values=['odd'],aggfunc=np.max)
    s= table.style.apply(fill_exceedances, axis=None).format("{:.1f}").set_properties(**{'text-align': 'center','border-color': 'black','border-style' :'solid' ,'border-width': '1px','border-collapse':'collapse'})
    f.write(s.render()) # df is the styled dataframe
    
    for horse_nos in trim_table_temp['current_race_horse'].unique():

        trim_table = trim_table_temp.loc[trim_table_temp['current_race_horse'] == horse_nos]    
        table = pd.pivot_table(trim_table,index=['next_race_horse'],columns=['race','current_race_horse','timestamp'],values=['odd'],aggfunc=np.max)
        s = table.style.apply(fill_exceedances, axis=None).format("{:.1f}").set_properties(**{'text-align': 'center','border-color': 'black','border-style' :'solid' ,'border-width': '1px','border-collapse':'collapse'})       
        f.write(s.render()) 

    f.close()
    
    os.system('python github_upload.py ' + folder_path + ' ' + 'double_odd_table' + str(x) + '.html')

pool_table = []
# Get Pool Amount
for x in range(int(race_start), int(race_nos)+1):
    #url of the page we want to scrape
    
    url = "https://bet.hkjc.com/racing/pages/odds_turnover.aspx?lang=ch&date=" + str(race_yr) + "-" + str(race_month) + "-" + \
        str(race_day) + "&venue=" + str(race_venue) + "&raceno=" + str(x) 

    driver.get(url)  
    # this is just to ensure that the page is loaded
    time.sleep(2) 
      
    html = driver.page_source

    soup = BeautifulSoup(html, "html.parser")

    df = pd.DataFrame(soup)
    
    
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
    with open(folder_path + 'pool_table.csv') as f:
        pool_table_csv = pd.read_csv (folder_path + 'pool_table.csv')
        merge_pool = [pool_table_df, pool_table_csv]  
        result_pool = pd.concat(merge_pool)
        result_pool.sort_values(by=['date', 'timestamp','race', 'turnover_pool'], ascending=[True, True, True, True], inplace=True)
        result_pool.to_csv(folder_path + 'pool_table.csv', index = False)
            
except IOError:
    result_pool = pool_table_df.copy()
    result_pool.sort_values(by=['date', 'timestamp','race', 'turnover_pool'], ascending=[True, True, True, True], inplace=True)
    result_pool.to_csv(folder_path + 'pool_table.csv', index = False)
