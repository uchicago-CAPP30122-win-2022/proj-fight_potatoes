#!/usr/bin/env python
# coding: utf-8

# In[20]:


import textblob
import csv
import pandas as pd
import re
import numpy as np


# if have time:
#     1. scale s&p500
#     2. remove neutral tweets and aggregate by day

# In[ ]:





# In[2]:


def get_weighted_ps_indicator(filename):
    """
    take average directly
    
    input:
        filename: string, for example: "data/tweets_china_021422.csv"
        
    return(tuple): average polarity and average subjectivity
    """
    
    tweets = pd.read_csv(filename)
    tweets.columns = ["time","id1","id2","popularity","content"]
    total_polarity = 0
    total_subjectivity = 0
    num_tweets = 0
    corpus = ''

    for idx, row in tweets.iterrows():
        text = row["popularity"]
        if not text:
            break
        weight = re.search(r"(?<='like_count': )\w+", text)  ############ mutable
        weight = 1 + int(weight.group(0)) ############ mutable
        blob = textblob.TextBlob(row["content"])
        polarity, subjectivity = blob.sentiment
        total_polarity += polarity * weight
        total_subjectivity += subjectivity * weight
        num_tweets += weight
        if weight > 500:    ######## mutable
            corpus += row["content"]

    ave_polarity = total_polarity / num_tweets 
    ave_subjectivity = total_subjectivity / num_tweets 
    
    return ave_polarity, ave_subjectivity, corpus


# In[16]:


def collect_y(dates, y_datafile, stock):
    """
    """

    y_num = []
    y_dummy = [] 

    for idx, day in enumerate(dates):
        day = str(day)
        day_text = "0"+f"{day[0]}"+"/"+f"{day[1:]}"+"/2022"
        if idx == 0:
            preceding_index = y_datafile.index.get_loc(day_text) + 1
            preceding_date = y_datafile.index[preceding_index]
            y_num.append(y_datafile.loc[preceding_date][stock])
        y_num.append(y_datafile.loc[day_text][stock])

    starting_y = y_num[0]        
    for y in y_num[1:]:
        if y > starting_y:
            y_dummy.append(1)
        else:
            y_dummy.append(0)
        starting_y = y
        
    y_num = np.array(y_num[1:])
    
    return y_dummy, y_num
    
    


# In[13]:


def collect_x(dates, topic):
    """
    """
    all_ave_polarity = []
    all_ave_subjectivity = []
    corpus = []
    for date in dates:
        filename = f"data/tweets_{topic}_0{date}22.csv"
        ave_polarity, ave_subjectivity, corpus_sub = get_weighted_ps_indicator(filename)
        all_ave_polarity.append(ave_polarity)
        all_ave_subjectivity.append(ave_subjectivity)
        corpus.append(corpus_sub)
    Xs = np.column_stack([all_ave_polarity, all_ave_subjectivity])
    
    return Xs, corpus
    
    


# In[ ]:


def 


# In[ ]:


np.array([[pol1, sub1, X3],[pol1, sub1, X3],[pol1, sub1, X3])


# In[14]:


def collect_all_x_and_y(dates, topics, y_filename, stocks):
    """
    collect the dependent variable and independent variable of specified dates and topics average directly
    
    input:
        dates: a list of dates, the date should only be trading dates.
                for example, [214,215,216,217,218,222,223,224,225,228,301,302]
        topic: string, either "covid" or "china"
        y_filename: for example: 'data/S&P_update.csv'
        
    return(tuple): a tuple of average polarity and average subjectivity
    """
    print("---> working on extracting sentiment indicator")
    x_dic = {}
    for topic in topics:
        x_dic[topic] = collect_x(dates, topic)
        
    print("---> working on extracting dependent variable")
    y_dic = {}
    y_datafile = pd.read_csv(y_filename, header = 0, thousands=',')
    y_datafile.set_index("Date", inplace = True)
    for stock in stocks:
        y_dic[stock] = collect_y(dates, y_datafile, stock)
    
    return y_dic, x_dic


# In[17]:


# y_dic, x_dic = collect_all_x_and_y(dates = TRAINING_DATES, topics = TOPIC, y_filename = Y_FILENAME, stocks = STOCK)


# In[ ]:


df["03/09/2022"]


# In[ ]:


df["03/09/2022"]


# In[ ]:


preceding_index = y_datafile.index.get_loc(day_text) + 1
preceding_date = y_datafile.index[preceding_index]

what_we_want = (y_datafile.loc[preceding_date][stock])


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




