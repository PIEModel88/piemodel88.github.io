import datetime, schedule, time, os
import csv
import pandas as pd
import numpy as np

from datetime import timedelta 
from datetime import datetime

import pytz
import os 



run_option = 2
race_yr = '2021'
race_month = '05'
race_day = '19'
race_venue = 'HV'
race_start = '1'
race_nos = '9'

tz_HK = pytz.timezone('Asia/Hong_Kong') 
folder_path = '/Users/ivamn/Documents/horse/Test/'
static_time = datetime.now(tz_HK)
static_time = static_time.replace(tzinfo=None)

# TIME = [(str(int(race_day) - 1) + '.' + race_month + '.' + race_yr, '06:11'),
#         (str(int(race_day) - 1) + '.' + race_month + '.' + race_yr, '12:30'),
#         (str(int(race_day) - 1) + '.' + race_month + '.' + race_yr, '18:30'),
#         (race_day + '.' + race_month + '.' + race_yr, '00:00'),
#         (race_day + '.' + race_month + '.' + race_yr, '06:11'),
#         (race_day + '.' + race_month + '.' + race_yr, '07:01'),
#         (race_day + '.' + race_month + '.' + race_yr, '08:00'),
#         (race_day + '.' + race_month + '.' + race_yr, '09:00'),
#         (race_day + '.' + race_month + '.' + race_yr, '10:00'),
#         (race_day + '.' + race_month + '.' + race_yr, '11:00'),
#         (race_day + '.' + race_month + '.' + race_yr, '12:00')]
def job():
    global TIME
    date = datetime.now().strftime("%d.%m.%Y %H:%M")
    static_time = datetime.now(tz_HK)
    static_time = static_time.replace(tzinfo=None)
    for i in TIME:
        runTime = i[0] + " " + i[1]
        if i and date == str(runTime):
            os.system('python hkjc_schedule.py ' + race_start + ' ' + race_nos + ' ' + race_yr + ' ' + race_month + ' ' + race_day + ' ' + race_venue + ' ' + folder_path)
            race_time_table = pd.read_csv (folder_path + 'race_time.csv')
            race_time_table['last_time'] = static_time.strftime("%Y/%m/%d, %H:%M:%S")
            race_time_table.to_csv (folder_path + 'race_time.csv', index = False)


def job2():
    static_time = datetime.now(tz_HK)
    static_time = static_time.replace(tzinfo=None)
    os.system('python hkjc_schedule.py ' + race_start + ' ' + race_nos + ' ' + race_yr + ' ' + race_month + ' ' + race_day + ' ' + race_venue + ' ' + folder_path)
   

if run_option == 1:
    schedule.every(1).minutes.do(job)
    
    while True:
        schedule.run_pending()
        time.sleep(1)
elif run_option == 2:
    schedule.every(1).seconds.do(job2)    
    while True:
        schedule.run_pending()
        time.sleep(1)   
elif run_option == 3:
    os.system('python Extract_HKJC_Double.py ' + race_start + ' ' + race_nos + ' ' + race_yr + ' ' + race_month + ' ' + race_day + ' ' + race_venue + ' ' + folder_path)
    race_time_table = pd.read_csv (folder_path + 'race_time.csv')
    race_time_table['last_time'] = static_time.strftime("%Y/%m/%d, %H:%M:%S")
    race_time_table.to_csv (folder_path + 'race_time.csv', index = False)    
elif run_option == 4: 
    #hist_double_odd = pd.read_csv (r'/Users/ivamn/Documents/horse/Test/ext_combined_double_odd.csv')
    hist_double_odd_1 = pd.read_csv (folder_path + 'ext_double_odd_' + str(1)  + '.csv')
    hist_double_odd_2 = pd.read_csv (folder_path + 'ext_double_odd_' + str(2)  + '.csv')
    hist_double_odd_3 = pd.read_csv (folder_path + 'ext_double_odd_' + str(3)  + '.csv')
    hist_double_odd_4 = pd.read_csv (folder_path + 'ext_double_odd_' + str(4)  + '.csv')
    hist_double_odd_5 = pd.read_csv (folder_path + 'ext_double_odd_' + str(5)  + '.csv')
    hist_double_odd_6 = pd.read_csv (folder_path + 'ext_double_odd_' + str(6)  + '.csv')
    hist_double_odd_7 = pd.read_csv (folder_path + 'ext_double_odd_' + str(7)  + '.csv')
    hist_double_odd_8 = pd.read_csv (folder_path + 'ext_double_odd_' + str(8)  + '.csv')
    hist_double_odd_9 = pd.read_csv (folder_path + 'ext_double_odd_' + str(9)  + '.csv')
    
    #    merge_odd = [hist_double_odd,hist_double_odd_1, hist_double_odd_2,hist_double_odd_3,hist_double_odd_4,hist_double_odd_5,hist_double_odd_6,hist_double_odd_7,hist_double_odd_8,hist_double_odd_9]  
    merge_odd = [hist_double_odd_1, hist_double_odd_2,hist_double_odd_3,hist_double_odd_4,hist_double_odd_5,hist_double_odd_6,hist_double_odd_7,hist_double_odd_8,hist_double_odd_9]  
    result_odd = pd.concat(merge_odd)
    result_odd.sort_values(by=['timestamp','race', 'current_race_horse','next_race_horse'], ascending=[True, True, True, True], inplace=True)
    result_odd.to_csv(folder_path + 'ext_combined_double_odd.csv', index = False)  
elif run_option == 5: 
    os.system('python github_upload.py ' + folder_path + ' ' + 'double_odd_table' + str(x) + '.html')