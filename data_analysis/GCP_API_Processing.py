import argparse
import pandas as pd
import operator
import numpy as np
import re

from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types


import google.api_core.exceptions

print('hello shern')

client = language.LanguageServiceClient()

#with open('UK_Ttest.csv', 'r') as review_file:
   # Instantiates a plain text document.
  #  content = review_file.read()

df = pd.read_csv('Malaysia_period.csv')

df['sentiment_score'] = ''
df['sentiment_magnitude'] = ''
df['key_feature'] = ''
df['key_feature_score'] = ''
df['key_feature_salience'] = ''
df['key_feature_magnitude'] = ''
df['place_mentioned'] = ''
df['top_1_entity'] = ''
df['top_1_entity_score'] = ''
df['top_2_entity'] = ''
df['top_2_entity_score'] = ''
df['top_3_entity'] = ''
df['top_3_entity_score'] = ''
df['language'] = ''



type_ = enums.Document.Type.PLAIN_TEXT
encoding_type = enums.EncodingType.UTF8

j = 0
for i in df['tweet']:
    saliencedict = {}
    document = {"content": i, "type": type_}

    try:
        entity_sentiment_response = client.analyze_entity_sentiment(document, encoding_type=encoding_type)
        sentiment_response = client.analyze_sentiment(document, encoding_type=encoding_type)
    except google.api_core.exceptions.InvalidArgument:
        df['key_feature'][j] = 'Invalid_language!'
        continue

    #################SENTIMENT ANALYSIS #########################
    df['sentiment_score'][j] = sentiment_response.document_sentiment.score
    df['sentiment_magnitude'][j] = sentiment_response.document_sentiment.magnitude

    ################ ENTITY SENTIMENT ANALYSIS####################

    for entity in entity_sentiment_response.entities:
        if re.search('movement', entity.name, re.IGNORECASE) or re.search('mco', entity.name, re.IGNORECASE) or re.search('rmo', entity.name, re.IGNORECASE):
        #if (entity.name.lower() == 'lockdown' or entity.name.lower() == 'wfh' or entity.name.lower() == '#wfh' or entity.name.lower() == 'working from home'):
            df['key_feature'][j] = entity.name
            df['key_feature_score'][j] = entity.sentiment.score
            df['key_feature_salience'][j] = entity.salience
            df['key_feature_magnitude'][j] = entity.sentiment.magnitude
        
        if entity.type == 'LOCATION':
            df['place_mentioned'][j] = entity.name
        
        saliencedict[entity.name] = entity.salience

    try:
        df['top_1_entity'][j] = sorted(saliencedict.items(), key=operator.itemgetter(1))[-1][0] #get highest key
        df['top_1_entity_score'][j] = sorted(saliencedict.items(), key=operator.itemgetter(1))[-1][1] #get highest value
    except IndexError:
        df['top_1_entity'][j] = None
        df['top_1_entity_score'][j] = None

    try:
        df['top_2_entity'][j] = sorted(saliencedict.items(), key=operator.itemgetter(1))[-2][0] #get highest key
        df['top_2_entity_score'][j] = sorted(saliencedict.items(), key=operator.itemgetter(1))[-2][1] #get highest value
    except IndexError:
        df['top_2_entity'][j] = None
        df['top_2_entity_score'][j] = None

    try:
        df['top_3_entity'][j] = sorted(saliencedict.items(), key=operator.itemgetter(1))[-3][0] #get highest key
        df['top_3_entity_score'][j] = sorted(saliencedict.items(), key=operator.itemgetter(1))[-3][1] #get highest value
    except IndexError:
        df['top_3_entity'][j] = None
        df['top_3_entity_score'][j] = None



    df['language'][j] = sentiment_response.language
    j += 1
    print(j)




df.to_csv('Malaysia_Lockdown_results.csv', index=False, encoding='utf-8')