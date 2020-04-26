"""This script uses the output csv file produced by extracttweet.py. It iterates through the users in the csv file and scraps the 
user profile data. The information that we are interested in is the 'Location' of the user. This script can be merged with extracttweet.py,
but kept apart for clarity reasons.
"""


import twint
import pandas as pd
import tqdm


filename = 'Global_Lockdown'
tweetdf = pd.read_csv(filename+'.csv')


tweetdf = tweetdf.drop_duplicates(['username', 'tweet'], keep = False) #dropping possible bot behaviour. same username tweeting exactly same tweets are very likely bots


username = tweetdf.iloc[:, 7].unique() #unique list of usernames


for i in tqdm.tqdm(username):    
    c = twint.Config()
    c.Username = i
    c.Format = " Username {username} | Location {location}"
    c.Output = filename + '_user_location.csv'
    c.Store_csv = True
    c.Hide_output = True
    twint.run.Lookup(c)


    


