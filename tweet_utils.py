#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
from textblob import TextBlob


class Sentiments:
    POSITIVE = 'Positive'
    NEGATIVE = 'Negative'
    NEUTRAL = 'Neutral'
    CONFUSED = 'Confused'


pos = '😀|😁|😂|😃|😄|😅|😆|😇|😈|😉|😊|😋|😌|😍|😎|😏|😗|😘|😙|😚|😛|😜|😝|😸|😹|😺|😻|😼|😽'
neg = '😒|😓|😔|😖|😞|😟|😠|😡|😢|😣|😤|😥|😦|😧|😨|😩|😪|😫|😬|😭|😾|😿|😰|😱|🙀'
neutral = '😐|😑|😳|😮|😯|😶|😴|😵|😲'
confused = '😕'

emoticons = {Sentiments.POSITIVE: pos,
             Sentiments.NEGATIVE: neg,
             Sentiments.NEUTRAL: neutral,
             Sentiments.CONFUSED: confused
             }


def sentiment_analysis(tweet):
    tweet['emoticons'] = []
    tweet['sentiments'] = []
    sentiment = _sentiment_analysis_by_emoticons(tweet)
    if len(tweet['sentiments']) == 0:
        sentiment = _sentiment_analysis_by_text(tweet)
    return sentiment


def _sentiment_analysis_by_emoticons(tweet):
    for sentiment, emoticons_icons in emoticons.items():
        matched_emoticons = re.findall(emoticons_icons, tweet['text'])
        if len(matched_emoticons) > 0:
            tweet['emoticons'].extend(matched_emoticons)
            tweet['sentiments'].append(sentiment)

    if Sentiments.POSITIVE in tweet['sentiments'] and Sentiments.NEGATIVE in tweet['sentiments']:
        tweet['sentiments'] = Sentiments.CONFUSED
    elif Sentiments.POSITIVE in tweet['sentiments']:
        tweet['sentiments'] = Sentiments.POSITIVE
    elif Sentiments.NEGATIVE in tweet['sentiments']:
        tweet['sentiments'] = Sentiments.NEGATIVE
    return tweet['sentiments']


def _sentiment_analysis_by_text(tweet):
    blob = TextBlob(tweet['text'])
    sentiment_polarity = blob.sentiment.polarity
    if sentiment_polarity < 0:
        sentiment = Sentiments.NEGATIVE
    elif sentiment_polarity <= 0.2:
                sentiment = Sentiments.NEUTRAL
    else:
        sentiment = Sentiments.POSITIVE
    tweet['sentiments'] = sentiment
    return tweet['sentiments']
