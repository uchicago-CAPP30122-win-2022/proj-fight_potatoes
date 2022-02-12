import tweepy
import csv
client = tweepy.Client(bearer_token='AAAAAAAAAAAAAAAAAAAAAPrIYwEAAAAAjiWmjHoKgV4fiZhdS6firx8RdCA%3DONdrIa4BTcne0syOtITPMKWHAsFdTA7FlA8gq4z2y4etPEIn6F')

# Replace with your own search query
'''
# covid query
query = 'covid19 OR covid OR covid-19 OR vaccine OR vaccination OR omicron OR booster\
OR mask OR mandate OR lockdown OR death rate OR travel restriction OR total infections OR\
breakthrough infections OR social distancing OR quarantine OR isolation OR pandemic OR shutdown\
lang:en -is:retweet'
'''

# us-china query
query = 'China (Trump OR Biden OR trade war OR Xi Jinping OR Eileen Gu OR Taiwan\
OR Hong Kong OR CCP OR TikTok OR Huawei OR tariffs OR human rights lang:en -is:retweet)'

file_name = 'tweets.csv'

with open(file_name, 'w') as f:
    writer = csv.writer(f)
    for tweet in tweepy.Paginator(client.search_recent_tweets, query=query,
            tweet_fields=['text', 'created_at', 'id', 'public_metrics'],
            max_results=100).flatten(limit=10000):
        writer.writerow([tweet.created_at, tweet.author_id, tweet.id, tweet.public_metrics, tweet.text.encode('utf-8')])
