#!/usr/bin/env python
# coding: utf-8

# In[13]:


import datetime
from datetime import date
import pandas as pd
import yfinance as yf


# In[17]:


import collecting_tweets
import update


# In[8]:


industry_filename = 'data/constituents.csv'


# In[9]:


update_tweet = input("Do you want to download today's data to update the data base? Enter Yes or No") or "No"


# In[16]:


if update_tweet.lower() == "yes":
    # comp = pd.read_csv("data/constituents.csv")
    comp = pd.read_csv(industry_filename)
    comp_lst = pd.Series(comp['Symbol']).str.replace(".", '-')
    comp_lst = list(comp_lst)
    comp_lst = ['SPY'] + comp_lst
    
    today = str(date.today())
    
    file = auto_update(today)
    


# In[3]:


today = str(date.today())
    
today


# In[ ]:





# In[ ]:





# In[4]:


def auto_update(today):
    """
    """
    
    print("----------------------------------- start to collect today's tweet data -----------------------------------")
    collecting_tweets.collect_tweets("china", today)
    collecting_tweets.collect_tweets("covid", today)

    print("----------------------------------- start to collect today's stock data -----------------------------------")
    # collect stock data
    y_file = yf.download(comp_lst, start='2022-02-04', end = today)    
    
    y_file = update.clean_stock_information(y_file)
    y_file = update.add_sector_y_datafile(y_file, comp)
    ### combine y_file 和 df_oneday
    
    print("-----------------------------------finishing update-----------------------------------")
    
    return y_file
    
    

