# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 22:27:19 2020

@author: Khai Xi
"""

import twint
import pandas as pd
import tqdm


filename = 'LOCKDOWN_WFH_test'
tweetdf = pd.read_csv(filename+'.csv')



tweetdf = tweetdf.drop_duplicates(['username', 'tweet'], keep = False)


username = tweetdf.iloc[:, 7].unique()

#username = username.values
j = 0

for i in tqdm.tqdm(username):    
    c = twint.Config()
    c.Username = i
    c.Format = " Username {username} | Location {location}"
    #
    
    c.Output = filename + '_user_location.csv'
    c.Store_csv = True
    c.Store_object = True
    c.Hide_output = True
    twint.run.Lookup(c)
    users = twint.output.users_list
    #print(users[j].location)
    #j = j+1

    


"""
c = twint.Config()
c.Username = "GinaYapLaiYoong"
c.Format = "ID {id} | Username {username} | Location {location}"

user = twint.run.Lookup(c)
print(type(user))

"""