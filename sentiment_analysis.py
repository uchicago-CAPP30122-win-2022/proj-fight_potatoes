'''
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
sid = SentimentIntensityAnalyzer()
import re
import pandas as pd
import nltk
nltk.download('words')
words = set(nltk.corpus.words.words())
'''

from textblob import TextBlob
import sys
import tweepy
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import nltk
import re
import string

from wordcloud import WordCloud, STOPWORDS
from PIL import Image
from nltk.sentiment.vader import SentimentIntensityAnalyzer
sid = SentimentIntensityAnalyzer()
#nltk.download('words')
words = set(nltk.corpus.words.words())

df = pd.read_csv('data/tweets_china_021622.csv')
df.columns = ['created_at', 'author_id', 'tweet_id', 'public_metrics','text']

####### NEED TO GET RID OF ENCODING PROBLEM ########
def cleaner(tweet):
    tweet = re.sub("@[A-Za-z0-9]+","",tweet) #Remove @ sign
    tweet = re.sub(r"(?:\@|http?\://|https?\://|www)\S+", "", tweet) #Remove http links
    tweet = " ".join(tweet.split())
    tweet = tweet.replace("#", "").replace("_", " ") #Remove hashtag sign but keep the text
    tweet = " ".join(w for w in nltk.wordpunct_tokenize(tweet)
        if w.lower() in words or not w.isalpha())
    return tweet
    
df['text_clean'] = df['text'].apply(cleaner)

sent = []
for i in df['text_clean']:
    sent.append((sid.polarity_scores(str(i)))['compound'])

df['sentiment'] = pd.Series(sent)

def sentiment_category(sentiment):
    label = ''
    if(sentiment > 0):
        label = 'positive'
    elif(sentiment == 0):
        label = 'neutral'
    else:
        label = 'negative'
    return(label)

df['sentiment_cat'] = df['sentiment'].apply(sentiment_category)

# split dfs
neg = df[df['sentiment_cat']=='negative']
neg = neg.groupby(['created_at'],as_index=False).count()
pos = df[df['sentiment_cat']=='positive']
pos = pos.groupby(['created_at'],as_index=False).count()
pos = pos[['created_at','tweet_id']]
neg = neg[['created_at','tweet_id']]

tw_list_negative = df[df['sentiment_cat']=='negative']
tw_list_positive = df[df['sentiment_cat']=='positive']
tw_list_neutral = df[df['sentiment_cat']=='neutral']

# word cloud
text_neg = " ".join(tw for tw in tw_list_negative.text_clean)
stopwords = set(STOPWORDS)
wordcloud = WordCloud(stopwords=stopwords, background_color="white").generate(text_neg)

def count_values_in_column(data, feature):
    total=data.loc[:,feature].value_counts(dropna=False)
    percentage=round(data.loc[:,feature].value_counts(dropna=False,normalize=True)*100,2)
    return pd.concat([total,percentage],axis=1,keys=['Total','Percentage'])
#Count_values for sentiment
count_values_in_column(df,'sentiment')



'''
def create_wordcloud(text):
    mask = np.array(Image.open('cloud.png'))
    stopwords = set(STOPWORDS)
    wc = WordCloud(background_color='white',
        mask = mask,
        max_words=3000,
        stopwords=stopwords,
        repeat=True)
    wc.generate(str(text))
    wc.to_file('wc.png')
    print('Word Cloud Saved Successfully')
    path='wc.png'
    display(Image.open(path))

create_wordcloud(df['text_clean'].values)
create_wordcloud(tw_list_positive['text_cleanxt'].values)
create_wordcloud(tw_list_negative['text_clean'].values)
create_wordcloud(tw_list_neutral['text_clean'].values)
