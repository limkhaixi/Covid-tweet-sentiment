

from geotext import GeoText
import pandas as pd
import numpy as np


tweetdf = pd.read_csv("LOCKDOWN_WFH_test.csv")
userdf = pd.read_csv("LOCKDOWN_WFH_test_user_location.csv")


tweetdf = tweetdf.drop_duplicates(['username', 'tweet'], keep = False)
userdf = userdf.drop_duplicates(subset=['username'])


master = pd.merge(tweetdf, userdf, on='username', how='left')

master = master[['username', 'date', 'tweet', 'location']]


master = master.dropna(subset=['location'])


def countrysort(x):
    country = GeoText(x).country_mentions
    if len(country) != 0:
        result = list(country.keys())
        return result[0]
    

master['Country'] = master.apply(lambda x: countrysort(x['location']), axis = 1) #or 1

master = master.sort_values(['Country', 'date'], ascending = [True, True])

#master.Country.value_counts()[:50]

processeddf = master.loc[master['Country'] == 'GB']

processeddf.to_csv('UK_period.csv', index=False)






