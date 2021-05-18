#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 13 15:11:23 2021

@author: ivamn
"""

#pip install schedule

import schedule
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('ggplot')
#pip install pivottablejs
from pivottablejs import pivot_ui
from datetime import timedelta 
from datetime import datetime
from github import Github
import os, sys
import csv

from bs4 import BeautifulSoup
from html_table_parser import HTMLTableParser
from datetime import timedelta 
from datetime import datetime
import pytz
from sys import exit

race_yr = '2021'
race_month = '05'
race_day = '19'
race_venue = 'HV'
race_start = '1'
race_nos = '1'

date_format = "%d/%m/%Y"
tz_HK = pytz.timezone('Asia/Hong_Kong') 
static_time = datetime.now(tz_HK).strftime("%Y/%m/%d, %H:%M:%S")
hist_double_odd = pd.read_csv (r'/Users/ivamn/Documents/horse/Test/ext_double_odd_' + race_start + '.csv')
folder_path = '/Users/ivamn/Documents/horse/Test/'


# for index, row in hist_double_odd.iterrows():
#     hist_double_odd.loc[index,'timestamp_second'] = datetime.strptime(row['timestamp'],'%Y/%m/%d, %H:%M:%S').timestamp()

# hist_double_odd.to_csv(r'/Users/ivamn/Documents/horse/Test/python_ext_double_odd' + '.csv', index = False)

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
    #g = Github("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")
    #repo = g.get_user().get_repo("piemodel88.github.io")
    
    trim_table_temp = pd.read_csv (r'/Users/ivamn/Documents/horse/Test/ext_double_odd_' + str(x) + '.csv')
    f=open(folder_path + 'double_odd_table' + str(x) + '.html','w')
    disable_cache1 = "<meta http-equiv=" + '"' + "Cache-Control" + '"' + " content=" + '"' + "no-cache, no-store, must-revalidate" + '"' + ">"
    disable_cache2 = "<meta http-equiv=" + '"' + "Pragma" + '"' + " content=" + '"' + "no-cache" + '"' + ">"
    disable_cache3 = "<meta http-equiv=" + '"' + "Expires" + '"' + " content=" + '"' + "0" + '"' + ">"
    f.write(disable_cache1)
    f.write(disable_cache2)
    f.write(disable_cache3)  
    page_refresh = "<meta content=" + '"' + "10" + '"' + " http-equiv=" + '"' + "refresh" + '"' + ">"
    f.write(page_refresh)
    f.write('2021/05/18, 18:30:01')
    url_link = "<A HREF=" + '"' + "../index.html" + '"' + ">Home            </A>"
    f.write(url_link)
    if int(x) >=2:
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
        f.write(s.render()) # df is the styled dataframe
    
    
    # table = pd.pivot_table(trim_table,index=['next_race_horse'],columns=['race','current_race_horse','timestamp'],values=['odd'],aggfunc=np.max)
    # s= table.style.apply(fill_exceedances, axis=None).format("{:.1f}").set_properties(**{'text-align': 'center'})
    # f=open('/Users/ivamn/Documents/horse/Test/double_odd_table' + str(x) + '.html','w')
    # f.write(s.render()) # df is the styled dataframe
    
    f.close()
    os.system('python github_upload.py ' + folder_path + ' ' +  'double_odd_table' + str(x) + '.html')
# soup = BeautifulSoup(open('/Users/ivamn/Documents/horse/Test/double_odd_table' + str(x) + '.html'), 'html.parser')
# metatag = soup.new_tag('meta')
# metatag.attrs['http-equiv'] = 'refresh'
# metatag.attrs['content'] = '30'
# soup.append(metatag)
# soup.append(static_time)
# with open("/Users/ivamn/Documents/horse/Test/double_odd_table" + str(x) + ".html", "w") as file:
#     file.write(str(soup))

#os.system('python github_upload.py ' + folder_path + ' ' + 'double_odd_table' + str(x) + '.html')
# for x in hist_double_odd['race'].unique():
#     trim_table_temp = hist_double_odd.loc[hist_double_odd['race'] == x]
#     arr = trim_table_temp['timestamp_second'].unique()
#     sorted_array = arr[np.argsort(arr)][-20: ]
#     trim_table = trim_table_temp[trim_table_temp['timestamp_second'].isin(sorted_array)]
#     table = pd.pivot_table(trim_table,index=['next_race_horse'],columns=['race','current_race_horse','timestamp'],values=['odd'],aggfunc=np.max)
#     s= table.style.apply(fill_exceedances, axis=None).format("{:.1f}").set_properties(**{'text-align': 'center'})
    
#     f=open('/Users/ivamn/Documents/horse/Test/double_odd_table_test' + str(x) + '.html','w')
#     f.write(s.render()) # df is the styled dataframe

#     disable_cache1 = "<meta http-equiv=" + '"' + "Cache-Control" + '"' + " content=" + '"' + "no-cache, no-store, must-revalidate" + '"' + ">"
#     disable_cache2 = "<meta http-equiv=" + '"' + "Pragma" + '"' + " content=" + '"' + "no-cache" + '"' + ">"
#     disable_cache3 = "<meta http-equiv=" + '"' + "Expires" + '"' + " content=" + '"' + "0" + '"' + ">"
#     f.write(disable_cache1)
#     f.write(disable_cache2)
#     f.write(disable_cache3)    
#     page_refresh = "<meta content=" + '"' + "30" + '"' + " http-equiv=" + '"' + "refresh" + '"' + ">"
#     f.write(page_refresh)
#     f.write(static_time)
#     f.close()
    # soup = BeautifulSoup(open('/Users/ivamn/Documents/horse/Test/double_odd_table_test' + str(x) + '.html'), 'html.parser')

    # metatag = soup.new_tag('meta')
    # metatag.attrs['http-equiv'] = 'refresh'
    # metatag.attrs['content'] = '30'
    # soup.append(metatag)
    # soup.append(static_time)
    # with open("/Users/ivamn/Documents/horse/Test/double_odd_table_test" + str(x) + ".html", "w") as file:
    #     file.write(str(soup))
#    os.system('python github_upload.py ' + str(x))

#table = pd.pivot_table(hist_double_odd,index=['next_race_horse'],columns=['race','current_race_horse','timestamp'],values=['odd'],aggfunc=np.max)

#table.to_excel(r'/Users/ivamn/Documents/horse/Test/python_ext_double_odd_table' + '.xlsx', index = False)
    

# print(table.columns[0][2])
# print(s)
# for column in table.columns:
  
#     if count == 0:
#         table_boolean [column] = False
#         prev_column = column
#         count = count + 1
#     else:       
#         table_boolean [column] =  table [column] > table[prev_column]
#         prev_column = column
#         count = count + 1
        
# #table1 = table.style.apply((table.where(table_boolean, 'background-color: {}'.format('orange')).reindex(columns=table.columns)), axis=None)
    
# def fill_exceedances(x):
#     df1 = pd.DataFrame('', index=x.index, columns=x.columns)
#     #set color by mask and add missing non matched columns names by reindex
#     df1 = (df1.where(table_boolean, 'background-color: {}'.format(color))
#               .reindex(columns=x.columns, fill_value=''))
    
# s = table.style.apply(fill_exceedances, axis=None)

# def color_negative_red(val):
#     #color = 'red' if val > 50 else 'yellow'
#     color = 'red'
#     return 'color: %s' % color

# s = table.style.applymap(color_negative_red)


# f=open('/Users/ivamn/Documents/horse/Test/python_ext_double_odd_table.html','w')
# f.write(s.render()) # df is the styled dataframe
# f.close()


# with open('/Users/ivamn/Documents/horse/Test/python_ext_double_odd_table.html','w') as file:
#     file.write(table.to_html())

# writer = pd.ExcelWriter(r'/Users/ivamn/Documents/horse/Test/python_ext_double_odd_table' + '.xlsx')

# table.to_excel(writer, 'Sheet1')
# writer.save()

# print(table)  

# pivot_ui(hist_double_odd,outfile_path='/Users/ivamn/Documents/horse/Test/python_ext_double_odd_table.html’)
# HTML('/Users/ivamn/Documents/horse/Test/python_ext_double_odd_table.html’)

# for manager in table.index.get_level_values(0).unique():
#     temp_df = table.xs(manager)
#     temp_df.to_excel(writer,manager)

# writer.save()