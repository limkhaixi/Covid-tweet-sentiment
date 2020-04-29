# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 14:38:11 2020

@author: Khai Xi
"""
# -*- coding: utf-8 -*-
#

import twint
import os
import time
from datetime import datetime
from datetime import date, timedelta
import tqdm


os.chdir(r'C:\Users\Khai Xi\Documents\Bristol\Career\GCP')


d1 = datetime(2020, 3, 9, 00, 00, 00)
d2 = datetime.now()

# this will give you a list containing all of the dates
dd = [d1 + timedelta(days=x) for x in range((d2-d1).days + 1)]


def tweeteaxtract(x):
    c = twint.Config()
    #c.Location = True
    #c.Lang = 'en'                 
    c.Search = 'quarantena'
    #c.Search = 'lockdown', 
    #c.Search = 'working from home'
    #c.Search = 'WFH'
    #
    #c.Search = 'covid-19'
    #c.Search = 'coronavirus'
    c.Store_csv = True 
    c.Hide_output = True
    c.Output = 'Italian_quarantena.csv'
    
    c.Store_object = True
    
    #c.Since = '2020-03-17 00:00:00'
    #x = x.strftime("%Y-%m-%d %H:%M:%S")
    c.Until = x
    #c.Pandas = True
    twint.run.Search(c)

    #extracttweet script.
    
sizedict = {}

with open("Italian_quarantena.csv", "w") as my_empty_csv:
  # now you have an empty file already
  pass 

for i in tqdm.tqdm(range(0, len(dd))):
    activeday = dd[i].strftime("%Y-%m-%d %H:%M:%S")
    print(activeday)
    initialsize = os.stat('Italian_quarantena.csv').st_size
    print(initialsize)
    tweeteaxtract(activeday)
    endsize = os.stat('Italian_quarantena.csv').st_size
    diff = endsize - initialsize
    sizedict[activeday] = diff
    print(diff)
    print('going to sleep')
    time.sleep(500)
    print('awaken')

print(sizedict)

#j = 0
"""
while j>0:
    initialsize = os.stat('LOCKDOWN_WFH.csv').st_size
    time.sleep(10)
    endsize = os.stat('LOCKDOWN_WFH.csv').st_size
    if endsize-initialsize == 0:
        time.sleep(500)


#! /bin/env python3
import os
import sys

def like_cheese():
    var = input("Hi! I like cheese! Do you like cheese?").lower()
    if var == "yes":
        print("That's awesome!")

if __name__ == '__main__':
    like_cheese()
    os.execv(__file__, sys.argv)
    """
