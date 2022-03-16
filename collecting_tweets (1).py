#!/usr/bin/env python
# coding: utf-8

# In[2]:


import tweepy
import csv


# In[10]:


BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAACT2ZgEAAAAApKkqwYqidZuvq27T7SrfbE1qlh0%3DAdO1ZSkZIFbpTdAaQxkAAtEz8cAJeYukKcgv5NttDZhv9I5Pt6"

CLIENT = tweepy.Client(bearer_token=BEARER_TOKEN)


# In[11]:


def collect_tweets(topic, date, client = CLIENT):
    """
    """
    if topic == "covid":
        # covid query
        query = '(covid19 OR covid OR covid-19 OR vaccine OR vaccination OR omicron OR booster        OR mask OR mandate OR lockdown OR death rate OR travel restriction OR total infections OR        breakthrough infections OR social distancing OR quarantine OR isolation OR pandemic OR shutdown)        lang:en -is:retweet'

    else:
        # us-china query
        query = '(China (Trump OR Biden OR trade war OR Xi Jinping OR Eileen Gu OR Taiwan        OR Hong Kong OR CCP OR TikTok OR Huawei OR tariffs OR human rights OR Xinjiang OR Zhao Lijian        OR Ned Price)) lang:en -is:retweet'


    file_name = f'data/tweets_{topic}_0{date}22.csv'

    with open(file_name, 'w') as f:
#     with open(file_name, 'a+') as f:
        writer = csv.writer(f)
        for tweet in tweepy.Paginator(client.search_recent_tweets, query=query,
                tweet_fields=['text', 'created_at', 'author_id', 'id', 'public_metrics'],
                max_results=50).flatten(limit=200):
            writer.writerow([tweet.created_at, tweet.author_id, tweet.id, tweet.public_metrics, tweet.text.encode('utf-8')])


# In[14]:




