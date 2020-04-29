

import twint
import os
import time
from datetime import datetime
from datetime import date, timedelta
import tqdm



d1 = datetime(2020, 3, 9, 00, 00, 00)
d2 = datetime.now()

dd = [d1 + timedelta(days=x) for x in range((d2-d1).days + 1)]


def tweeteaxtract(x):
    c = twint.Config()               
    c.Search = 'quarantena'

    c.Store_csv = True 
    c.Hide_output = True
    c.Output = 'Italian_quarantena.csv'
    
    c.Store_object = True
    
    #c.Since = '2020-03-17 00:00:00'

    c.Until = x

    twint.run.Search(c)

    
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
