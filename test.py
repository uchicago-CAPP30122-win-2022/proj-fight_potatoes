#works
import tweepy
import csv
client = tweepy.Client(bearer_token='AAAAAAAAAAAAAAAAAAAAAPrIYwEAAAAAjiWmjHoKgV4fiZhdS6firx8RdCA%3DONdrIa4BTcne0syOtITPMKWHAsFdTA7FlA8gq4z2y4etPEIn6F')

# Replace with your own search query
query = 'trump -is:retweet'

file_name = 'tweets.csv'
'''
tweets = client.search_recent_tweets(query=query, tweet_fields=['text', 'created_at', 'author_id', 'id'], max_results=100)

for tweet in tweets.data:
    print(tweet.text)
'''
with open(file_name, 'w') as f:
    writer = csv.writer(f)
    for tweet in tweepy.Paginator(client.search_recent_tweets, query=query,
            tweet_fields=['text', 'created_at', 'author_id', 'id'], max_results=100).flatten(
            limit=1000):
        writer.writerow([tweet.created_at, tweet.author_id, tweet.id, tweet.text.encode('utf-8')])