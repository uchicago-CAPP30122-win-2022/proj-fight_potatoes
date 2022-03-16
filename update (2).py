#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd
import pandas_datareader as web
import re
from datetime import timedelta
from datetime import datetime
import yfinance as yf


# In[ ]:





# In[2]:





# In[ ]:





# In[5]:


def clean_stock_information(df):
    """
    
    """
    # drop repetitive col
    dropcolumn = []
    for name in df.columns:
        if (not 'Adj Close' in name) and (not "Date" in name):
            dropcolumn.append(name)
    
    df = df.drop(columns = dropcolumn)
    
    df.columns = [b for a, b in df.columns]
    df.reset_index(inplace=True)

    return df


# In[58]:


def add_sector_y_datafile(df, industry):
    """
    """

    df = df.fillna(0)
    
    for idx, row in industry.iterrows():
        row["Symbol"] = row["Symbol"].replace(".", "-")
        
    for sector in industry.Sector.unique():
        df[sector] = 0

    industry_group = industry.groupby('Sector')
    
    for idx, row in df.iterrows():
        for sector in industry.Sector.unique():
            stock_num = 0
            same_industry_stock = industry_group.get_group(sector)
            for stock in same_industry_stock.Symbol:
                if stock in df.columns and row[stock] != 0:
                    df[sector][idx] = row[sector] + row[stock]
                    stock_num += 1
            if stock_num != 0:                    
                row[sector] = row[sector] / stock_num

    df.to_csv('data/y_file_update.csv')


# In[ ]:





# In[ ]:





# In[60]:


# df_clean = clean_stock_information(df)
# df_sector = add_sector_y_datafile(df_clean, comp)


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




