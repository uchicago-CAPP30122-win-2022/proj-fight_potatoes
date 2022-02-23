import textblob
from textblob import TextBlob
import csv
import pandas as pd

tweets = pd.read_csv("data/tweets_china_022222.csv")
tweets.columns = ["time","id1","id2","popularity","content"]
tweet_sample = tweets["content"][2]

blob = textblob.TextBlob(tweet_sample)

# subtract noun phrases
blob.noun_phrases

# subtract sentences
blob.sentences

# sentiment analysis: 
# Polarity (range from [-1,1]) where 1 means positive statement and -1 means a negative statement. 
# Subjective sentences generally refer to personal opinion, emotion or judgment whereas objective refers to factual information

# sentiment for a sentence in the tweet
print(blob.sentences[0].sentiment)

# the overall sentiment for that tweet 
print(blob.sentiment)