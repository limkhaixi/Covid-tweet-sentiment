#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import matplotlib.pyplot as plt
import re

filename = 'UK'

df = pd.read_csv(filename+'_Lockdown_results.csv')

df


# In[3]:


df['sentiment_combined'] = df['sentiment_score']*df['sentiment_magnitude']
df['sentiment_score'].astype(str).astype(float)


# In[4]:


def entity_calculator(score):
    if score > 0.75:
        value =  3
    elif score <= 0.75 and score > 0.25:
        value =  2
    elif score <= 0.25:
        value =  1
    else:
        value = None
    return value


# In[6]:


import numpy as np

def clean_entity(entity):
    if pd.notnull(entity):
        if re.search('wfh', entity, re.IGNORECASE):
            entity = 'WFH'
        elif re.search('working from home', entity, re.IGNORECASE):
            entity = 'WFH'
        elif re.search('workingfromhome', entity, re.IGNORECASE):
            entity = 'WFH'
        elif re.search('work', entity, re.IGNORECASE):
            entity = 'WFH'
        elif re.search('lockdown', entity, re.IGNORECASE):
            entity = 'lockdown'
        elif re.search('meeting', entity, re.IGNORECASE):
            entity = 'meeting'
        elif entity == 'thing' or entity == 'lot' or entity == 'lots' or entity == 'way' or entity == 'part' or entity == 'one' or entity == 'ways' or entity == 'some' or entity == 'all' or entity == 'someone' or entity == 'things' or entity == 'lot' or entity == 'something' or entity == 'everything' or entity == 'bit' or entity == 'anything' or entity == 'many' or entity == 'fuck' or entity == 'shit' or entity == 'WTF' or entity == '#WTF' or entity == 'bullshit' or entity == 'M' or entity == 'FYI' or entity == 'idiot' or entity == 'ass' or entity == 'many' or entity == 'more':
            entity = None
        elif re.search('anyone', entity, re.IGNORECASE):
            entity = 'people'
        elif re.search('everyone', entity, re.IGNORECASE):
            entity = 'people'
        elif re.search('order', entity, re.IGNORECASE) or re.search('movement', entity, re.IGNORECASE) or re.search('mco', entity, re.IGNORECASE) or re.search('rmo', entity, re.IGNORECASE):
            entity = 'Movement Control Order'
        elif re.search('covid', entity, re.IGNORECASE) or re.search('virus', entity, re.IGNORECASE):
            entity = 'Covid-19'
        elif re.search('gov', entity, re.IGNORECASE):
            entity = 'Government'
        elif re.search('malaysia', entity, re.IGNORECASE):
            entity = 'Malaysia'
        elif re.search('malaysian', entity, re.IGNORECASE):
            entity = 'Malaysians'
        elif re.search('mum', entity, re.IGNORECASE) or re.search('dad', entity, re.IGNORECASE) or re.search('parent', entity, re.IGNORECASE):
            entity = 'parents'
        elif re.search('@narendramodi', entity, re.IGNORECASE) or re.search('@PMOIndia', entity, re.IGNORECASE):
            entity = '@PMOIndia'    
        elif re.search('airtel', entity, re.IGNORECASE):
            entity = '@airtelindia'    
        elif re.search('@jiocare', entity, re.IGNORECASE) or re.search('@reliancejio', entity, re.IGNORECASE):
            entity = '@jiocare'  
        elif entity == 'tip' or entity == 'tips':
            entity = 'Tips' 
        elif re.search('email', entity, re.IGNORECASE):
            entity = 'email' 
        elif re.search('internet', entity, re.IGNORECASE):
            entity = 'internet'
        elif re.search('thank', entity, re.IGNORECASE):
            entity = 'Thanks'
    return entity


# In[ ]:





# In[7]:


#df = df.loc[df['sentiment_score'] > 0]

df['top_1_entity_score'] = df.apply(lambda x: entity_calculator(x['top_1_entity_score']), axis = 1) #or 1
df['top_2_entity_score'] = df.apply(lambda x: entity_calculator(x['top_2_entity_score']), axis = 1) #or 1
df['top_3_entity_score'] = df.apply(lambda x: entity_calculator(x['top_3_entity_score']), axis = 1) #or 1

df['top_1_entity'] = df.apply(lambda x: clean_entity(x['top_1_entity']), axis = 1) #or 1
df['top_2_entity'] = df.apply(lambda x: clean_entity(x['top_2_entity']), axis = 1) #or 1
df['top_3_entity'] = df.apply(lambda x: clean_entity(x['top_3_entity']), axis = 1) #or 1





# In[8]:


negativesentiment = df.loc[df['sentiment_score'] <0]

negativegroup1 = negativesentiment.groupby('top_1_entity')['top_1_entity_score'].sum().sort_values(ascending = [False])

negativegroup2 = negativesentiment.groupby('top_2_entity')['top_2_entity_score'].sum().sort_values(ascending = [False])

negativegroup3 = negativesentiment.groupby('top_3_entity')['top_3_entity_score'].sum().sort_values(ascending = [False])

negativewordcloud = pd.concat([negativegroup1, negativegroup2, negativegroup3])
negativewordcloud = pd.DataFrame({'entity':negativewordcloud.index, 'value':negativewordcloud.values})

negativewordgroup = negativewordcloud.groupby('entity')['value'].sum().sort_values(ascending = [False])


negativewordgroup
#negativecsv.to_csv(filename + 'negative_wordcloud.csv')


# In[11]:


positivesentiment = df.loc[df['sentiment_score'] >0]

positivegroup1 = positivesentiment.groupby('top_1_entity')['top_1_entity_score'].sum().sort_values(ascending = [False])

positivegroup2 = positivesentiment.groupby('top_2_entity')['top_2_entity_score'].sum().sort_values(ascending = [False])

positivegroup3 = positivesentiment.groupby('top_3_entity')['top_3_entity_score'].sum().sort_values(ascending = [False])

positivewordcloud = pd.concat([positivegroup1, positivegroup2, positivegroup3])
positivewordcloud = pd.DataFrame({'entity':positivewordcloud.index, 'value':positivewordcloud.values})

positivewordgroup = positivewordcloud.groupby('entity')['value'].sum().sort_values(ascending = [False])
positivewordgroup
#positivecsv.to_csv(filename + 'positive_wordcloud.csv')


# In[12]:


pd.set_option('use_inf_as_na', True)

merged = pd.merge(negativewordgroup, positivewordgroup, on = 'entity', how = 'outer')
merged.fillna(0, inplace=True)
merged['final_value'] = merged['value_y'] - merged['value_x']
merged


# In[13]:


negative = merged.loc[merged['final_value'] < 0 ]
negative = negative.sort_values(by = 'final_value',ascending = True)
negativecsv = negative[0:30]
negativecsv['final_value'] = abs(negativecsv['final_value'])
#negativecsv.to_csv(filename + '_negative_wordcloud.csv')
negativecsv


# In[14]:


positive = merged.loc[merged['final_value'] > 0 ]
positive = positive.sort_values(by = 'final_value',ascending = False)
positivecsv = positive[0:30]
#positivecsv.to_csv(filename + '_positive_wordcloud.csv')
positivecsv


# In[ ]:





# In[ ]:





# In[17]:


daybyday = df[['date', 'sentiment_score', 'sentiment_magnitude', 'key_feature', 'key_feature_score', 'key_feature_salience', 'key_feature_magnitude']]

daybydaysentiment = df[['date', 'sentiment_score', 'sentiment_magnitude', 'sentiment_combined']]
daybydaysentiment = daybydaysentiment.groupby(['date'])['sentiment_score', 'sentiment_magnitude', 'sentiment_combined'].mean().reset_index()

pd.options.display.float_format = '{:.2f}'.format

daybydaysentiment.plot('date', 'sentiment_score')


# In[18]:


df['key_feature'] = df.apply(lambda x: clean_entity(x['key_feature']), axis = 1) #or 1
df['key_feature_combined'] = df['key_feature_score'] * df['key_feature_magnitude']

df.key_feature.value_counts()


# In[19]:



wfh_group = df.groupby(['date','key_feature'])['key_feature_score', 'key_feature_magnitude', 'key_feature_combined'].mean().reset_index()
wfhentitydf = wfh_group.loc[wfh_group['key_feature'] == 'WFH']


# In[20]:


lockdown_group = df.groupby(['date','key_feature'])['key_feature_score', 'key_feature_magnitude', 'key_feature_combined'].mean().reset_index()
lockdownentitydf = lockdown_group.loc[lockdown_group['key_feature'] == 'lockdown']


# In[21]:


data = pd.merge(wfhentitydf, daybydaysentiment, on = 'date', how = 'inner')


# In[22]:


data = pd.merge(data, lockdownentitydf, on = 'date', how = 'inner')


# In[23]:


data


# In[22]:


x = data['date'].values[2:]
y1 = data['sentiment_combined'].values[2:]
y2 = data['key_feature_combined_x'].values[2:]
y3 = data['key_feature_combined_y'].values[2:]


# In[25]:


plt.figure(figsize=(20,20))
plt.plot(x, y1, 'r', label = 'All tweets')
plt.plot(x, y2, 'g', label = 'Entity "Movement Control Order"')
plt.plot(x, y3, 'b', label = 'Entity "lockdown"')
plt.xticks(rotation=60, size = 20)
plt.yticks(size = 20)
plt.xlabel('Date', size = 20)
plt.ylabel('Average sentiment', size = 20)
plt.axvline(x = '2020-03-24', linestyle = '--', color = '#FCD64F')
plt.axvline(x = '2020-03-26', linestyle = '--', color = '#FCD64F')
plt.axvline(x = '2020-03-29', linestyle = '--', color = '#FCD64F')
plt.axvline(x = '2020-04-02', linestyle = '--', color = '#FCD64F')
plt.axvline(x = '2020-04-05', linestyle = '--', color = '#FCD64F')
plt.axvline(x = '2020-04-08', linestyle = '--', color = '#FCD64F')
plt.legend(loc = 'lower right', prop={'size': 20})
plt.title("Plot of average sentiment against "+filename+" lockdown period", size = 25, pad = 130)



plt.savefig(filename + '_plot.png')
plt.show()


# In[95]:


plt.savefig(filename + '_plot.png')
plt.show()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




