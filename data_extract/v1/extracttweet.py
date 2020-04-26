"""In an effort to bypass Twitter rate limitations, a function was written to extract relevant tweets by iterating through a list of dates.
After each iteration, the function was set to sleep for roughly 8 minutes to bypass Twitter rate limitations. On average, 8MB of tweets
were extracted for each day before Twitter rate limitations kicked in."""

import twint
import os
import time
from datetime import datetime
from datetime import date, timedelta
import tqdm

d1 = datetime(2020, 3, 9, 00, 00, 00) #startdate
d2 = datetime.now()                   #enddate

# returns list containing all of the dates
days = [d1 + timedelta(days=x) for x in range((d2-d1).days + 1)]

def tweeteaxtract(x):
    """main tweet extract function"""
    c = twint.Config()
    c.Lang = 'en'                 
    c.Search = 'lockdown', 
    c.Search = 'working from home'
    c.Search = 'WFH'
    c.Store_csv = True 
    c.Hide_output = True
    c.Output = 'Global_Lockdown.csv'
    c.Store_object = True
    c.Until = x
    twint.run.Search(c)

sizedict = {} #dictionary to store information of file size of tweets extracted by day

with open("Global_Lockdown.csv", "w") as my_empty_csv:
  # create empty csv
  pass 

for i in tqdm.tqdm(range(0, len(days))):
    activeday = days[i].strftime("%Y-%m-%d %H:%M:%S")       #extract relevant date and convert to datetime format
    initialsize = os.stat('Global_Lockdown.csv').st_size    
    tweeteaxtract(activeday)                                #main tweet function
    endsize = os.stat('Global_Lockdown.csv').st_size
    diff = endsize - initialsize
    sizedict[activeday] = diff                              #record size of tweets extracted for a day
    time.sleep(500)                                         #bypass Twitter rate limitations


print(sizedict)
