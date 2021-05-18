import pandas as pd
import numpy as np
from sys import exit
from datetime import timedelta 
from datetime import datetime
import pytz
import os, sys

date_format = "%d/%m/%Y"
#'%Y-%m-%d %H:%M:%S.%f'
tz_HK = pytz.timezone('Asia/Hong_Kong') 

Race_Finish = False
combined_time = ''
Update_file = False


#while Race_Finish != True:
static_time = datetime.now(tz_HK)
static_time = static_time.replace(tzinfo=None)
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
# race_nos = '8'
# folder_path = '/Users/ivamn/Documents/horse/Test/'

TIME = [(str(int(race_day) - 1) + '.' + race_month + '.' + race_yr, '06:11'),
        (str(int(race_day) - 1) + '.' + race_month + '.' + race_yr, '12:30'),
        (str(int(race_day) - 1) + '.' + race_month + '.' + race_yr, '18:30'),
        (race_day + '.' + race_month + '.' + race_yr, '00:00'),
        (race_day + '.' + race_month + '.' + race_yr, '06:11'),
        (race_day + '.' + race_month + '.' + race_yr, '07:01'),
        (race_day + '.' + race_month + '.' + race_yr, '08:00'),
        (race_day + '.' + race_month + '.' + race_yr, '09:00'),
        (race_day + '.' + race_month + '.' + race_yr, '10:00'),
        (race_day + '.' + race_month + '.' + race_yr, '11:00'),
        (race_day + '.' + race_month + '.' + race_yr, '12:00')]

date = datetime.now().strftime("%d.%m.%Y %H:%M")

for i in TIME:
    runTime = i[0] + " " + i[1]
    if i and date == str(runTime):
        race_time_table = pd.read_csv (folder_path + 'race_time.csv')
        race_time_table['last_time'] = static_time.strftime("%Y/%m/%d, %H:%M:%S")
        os.system('python Extract_HKJC_Double.py ' + race_start + ' ' + race_nos + ' ' + race_yr + ' ' + race_month + ' ' + race_day + ' ' + race_venue + ' ' + folder_path)
        
#        race_time_table['last_time'] = static_time.strftime("%Y/%m/%d, %H:%M:%S")
        race_time_table.to_csv (folder_path + 'race_time.csv', index = False)
        exit()    

try:
    with open(folder_path + 'race_time.csv') as f:
        race_time_table = pd.read_csv (folder_path + 'race_time.csv')
        
        for index, row in race_time_table.iterrows():
            combined_time = str(row['date']) + ' ' + str(row['time'])
            date_time_obj = datetime.strptime(combined_time, '%Y%m%d %H:%M')
 

            if date_time_obj.timestamp() - static_time.timestamp() >= 1800 and date_time_obj.timestamp() - static_time.timestamp() <= 21600:
                if static_time.timestamp()  - datetime.strptime(row['last_time'], '%Y/%m/%d, %H:%M:%S').timestamp() >= 3600:
                    race_time_table.loc[index,'last_time'] = static_time.strftime("%Y/%m/%d, %H:%M:%S")
                    os.system('python Extract_HKJC_Double.py ' + race_start + ' ' + race_start + ' ' + race_yr + ' ' + race_month + ' ' + race_day + ' ' + race_venue + ' ' + folder_path)
#                    race_time_table.loc[index,'last_time'] = static_time.strftime("%Y/%m/%d, %H:%M:%S")
                    Update_file = True
                # else:
                #     print (str(row['race_nos']) + '  ' + str(date_time_obj.timestamp() - static_time.timestamp()))
                
            elif date_time_obj.timestamp() - static_time.timestamp() >= 1900 and date_time_obj.timestamp() - static_time.timestamp() <= 2100:
                if static_time.timestamp() - datetime.strptime(row['last_time'], '%Y/%m/%d, %H:%M:%S').timestamp() >= 1900:
                    race_time_table.loc[index,'last_time'] = static_time.strftime("%Y/%m/%d, %H:%M:%S")
                    os.system('python Extract_HKJC_Double.py ' + race_start + ' ' + race_start + ' ' + race_yr + ' ' + race_month + ' ' + race_day + ' ' + race_venue + ' ' + folder_path)
#                    race_time_table.loc[index,'last_time'] = static_time.strftime("%Y/%m/%d, %H:%M:%S")
                    Update_file = True
                    
            elif date_time_obj.timestamp() - static_time.timestamp() >= -120 and date_time_obj.timestamp() - static_time.timestamp() <= 1020:
                if static_time.timestamp() - datetime.strptime(row['last_time'], '%Y/%m/%d, %H:%M:%S').timestamp() >= 59:
                    race_time_table.loc[index,'last_time'] = static_time.strftime("%Y/%m/%d, %H:%M:%S")
                    os.system('python Extract_HKJC_Double.py ' + race_start + ' ' + race_start + ' ' + race_yr + ' ' + race_month + ' ' + race_day + ' ' + race_venue + ' ' + folder_path)

                    Update_file = True
                # else:
                #     print (str(row['race_nos']) + '  ' + str(date_time_obj.timestamp() - static_time.timestamp()))
 
            # if date_time_obj.timestamp() - static_time.timestamp() < -120 and row['race_nos'] == 10:
            #     Race_Finish = True
        if Update_file == True:
            race_time_table.to_csv (folder_path + 'race_time.csv', index = False)
            Update_file = False
        else:
            Update_file = False
except IOError:
    print ('no file')
 # print(i)