import argparse
import pandas as pd
import operator
import numpy as np
import re

from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import google.api_core.exceptions


client = language.LanguageServiceClient()

df = pd.read_csv('UK_period.csv')

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


for counter, text in enumerate(df['tweet']):
    saliencedict = {}
    document = {"content": text, "type": type_}

    try: #error catch to catch non-english tweets
        entity_sentiment_response = client.analyze_entity_sentiment(document, encoding_type=encoding_type)
        sentiment_response = client.analyze_sentiment(document, encoding_type=encoding_type)
    except google.api_core.exceptions.InvalidArgument:
        df['key_feature'][counter] = 'Invalid_language!'
        continue

    #################SENTIMENT ANALYSIS #########################
    df['sentiment_score'][counter] = sentiment_response.document_sentiment.score #overall sentiment score
    df['sentiment_magnitude'][counter] = sentiment_response.document_sentiment.magnitude # overall sentiment magnitude

    ################ ENTITY SENTIMENT ANALYSIS####################

    for entity in entity_sentiment_response.entities:
        #if re.search('movement', entity.name, re.IGNORECASE) or re.search('mco', entity.name, re.IGNORECASE) or re.search('rmo', entity.name, re.IGNORECASE):  #extracting malaysian MCO entities
        if (entity.name.lower() == 'lockdown' or entity.name.lower() == 'wfh' or entity.name.lower() == '#wfh' or entity.name.lower() == 'working from home'):  #extrcting entities lockdown
            df['key_feature'][counter] = entity.name
            df['key_feature_score'][counter] = entity.sentiment.score
            df['key_feature_salience'][counter] = entity.salience
            df['key_feature_magnitude'][counter] = entity.sentiment.magnitude
        
        if entity.type == 'LOCATION':
            df['place_mentioned'][counter] = entity.name
        
        saliencedict[entity.name] = entity.salience #dictionary to capture entities and its salience (importance within text)

    try:
        df['top_1_entity'][counter] = sorted(saliencedict.items(), key=operator.itemgetter(1))[-1][0] #get highest key
        df['top_1_entity_score'][counter] = sorted(saliencedict.items(), key=operator.itemgetter(1))[-1][1] #get highest value
    except IndexError:
        df['top_1_entity'][counter] = None
        df['top_1_entity_score'][counter] = None

    try:
        df['top_2_entity'][counter] = sorted(saliencedict.items(), key=operator.itemgetter(1))[-2][0] #get highest key
        df['top_2_entity_score'][counter] = sorted(saliencedict.items(), key=operator.itemgetter(1))[-2][1] #get highest value
    except IndexError:
        df['top_2_entity'][counter] = None
        df['top_2_entity_score'][counter] = None

    try:
        df['top_3_entity'][counter] = sorted(saliencedict.items(), key=operator.itemgetter(1))[-3][0] #get highest key
        df['top_3_entity_score'][counter] = sorted(saliencedict.items(), key=operator.itemgetter(1))[-3][1] #get highest value
    except IndexError:
        df['top_3_entity'][counter] = None
        df['top_3_entity_score'][counter] = None


    df['language'][counter] = sentiment_response.language

df.to_csv('UK_Lockdown_results.csv', index=False, encoding='utf-8')
