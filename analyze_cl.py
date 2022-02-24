from textblob import TextBlob
import csv
import pandas as pd
import numpy as np
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import statsmodels.api as sm
import seaborn as sb

tweets = pd.read_csv("data/tweets_china_022122.csv")
tweets.columns = ["Date","id1","id2","popularity","content"]

sent = []
sub = []
for tweet in tweets.content:    
    blob = TextBlob(tweet)    
    sent.append(blob.sentiment[0])
    sub.append(blob.sentiment[1])

# add to tweets df
tweets['sentiment'] = pd.Series(sent)
tweets['subjectivity'] = pd.Series(sub)

# aggregate data by day
tweets['date'] = pd.to_datetime(tweets['Date'])
tweets['date'] = tweets['date'].dt.date

tweets1 = tweets.groupby('date').agg('mean')
# drop irrelevant cols
tweets1.drop(['id1', 'id2'], axis = 1, inplace = True)

# sp 500 data
sp = pd.read_csv('S&P 500 Historical Data.csv', header = 0, thousands=',')
sp['date'] = pd.to_datetime(sp['Date'])
sp['date'] = sp['date'].dt.date
sp.drop('Date', axis = 1, inplace = True)


# merge stock and tweet data
df = tweets1.merge(sp, how = "inner", on = "date")

# summary plots?
plt.scatter(x = 'sentiment', y = 'Price', data = df, s = 100, alpha = 0.3, edgecolor = 'white')
plt.title('Twitter Sentiments about China vs Stock Price', fontsize = 16)
plt.ylabel('Stock Price ($)', fontsize = 12)
plt.xlabel('Sentiment', fontsize = 12)

plt.savefig('sent_price.png')
#split train/test data
np.random.seed(5678)
train, test = train_test_split(df, test_size = 0.1, random_state = 42)


# build model
y_train = train.pop('Price')
x_train = train[['sentiment', 'subjectivity']]

#train model
#sklearn
lr = LinearRegression()
lr.fit(x_train,y_train)
yhat = lr.predict(test[['sentiment', 'subjectivity']])
print('Intercept: ', lr.intercept_)
print('Coefficients: ', lr.coef_)
#print('R-Squared :', lr.score(test[['sentiment', 'subjectivity']], test['Price']))

sb.distplot(yhat, hist = False, color = 'r', label = 'Predicted Values')
sb.distplot(test['Price'], hist = False, color = 'b', label = 'Actual Values')
plt.title('Actual vs Predicted Values', fontsize = 16)
plt.xlabel('Values', fontsize = 12)
plt.ylabel('Frequency', fontsize = 12)
plt.legend(loc = 'upper left', fontsize = 13)
plt.savefig('ap.png')

#statsmodels
x_var = df[['sentiment', 'subjectivity']]
y_var = df['Price']

sm_x_var = sm.add_constant(x_var)
mlr_model = sm.OLS(y_var, sm_x_var)
mlr_reg = mlr_model.fit()
print(mlr_reg.summary())
