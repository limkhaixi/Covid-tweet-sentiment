#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from googletrans import Translator
import re
import emoji
import time
import tqdm


df = pd.read_csv('Italian_quarantena.csv')


# In[2]:



def remove_symbol(x):
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)                  
        u"\U0001F1F2-\U0001F1F4"  # Macau flag
        u"\U0001F1E6-\U0001F1FF"  # flags
        u"\U0001F600-\U0001F64F"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U0001F1F2"
        u"\U0001F1F4"
        u"\U0001F620"
        u"\u200d"
        u"\u2640-\u2642"
                           "]+", flags=re.UNICODE)
    result = emoji_pattern.sub(r'', x)# no emoji
    result = result.replace('\n',' ')
    return result

def strip_emoji(text):
    #print(emoji.emoji_count(text))
    new_text = re.sub(emoji.get_emoji_regexp(), r"", text)
    return new_text


# In[8]:


def translator(x):
    x = strip_emoji(x)
    translator = Translator()
    result = translator.translate(x)
    return result.text


# In[4]:


df['translated'] = ''


# In[5]:


j = 0


for i in tqdm.tqdm(df['id']):
    df['translated'][j] = translator(df['tweet'][j])
    #print(df['tweet'][j])
    j += 1
    time.sleep(1)
   


# In[7]:





# In[27]:





# In[12]:


df['translated'] = df.apply(lambda x: translator(x['tweet']), axis = 1)


# In[11]:





# In[ ]:




