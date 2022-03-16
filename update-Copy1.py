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


# comp = pd.read_csv("data/constituents.csv")
comp = pd.read_csv("constituents.csv")
comp_lst = pd.Series(comp['Symbol']).str.replace(".", '-')
comp_lst = list(comp_lst)
comp_lst = ['SPY'] + comp_lst


# In[4]:


df = yf.download(comp_lst, start='2022-02-04', end='2022-03-15')


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


# In[29]:


def add_sector_y_datafile(df, industry):
    """
    """

#     df.set_index("Date", inplace = True)
    
    ######################### (check the number before submit) ######################
    # combine.drop(combine.tail(1).index,inplace=True) # delete the NA rows 
    # delete the NA columns
#     combine = combine.dropna(axis = "columns") 
    
    # prepare industry data
#     industry = pd.read_csv('data/constituents.csv')
    df = df.fillna(0)
#     print(df)
    
    for idx, row in industry.iterrows():
        row["Symbol"] = row["Symbol"].replace(".", "-")
        
    for sector in industry.Sector.unique():
        df[sector] = 0
    # add sector data
#     print(df)

    industry_group = industry.groupby('Sector')
    
    for idx, row in df.iterrows():
        for sector in industry.Sector.unique():
#             print(sector)
            stock_num = 0
            same_industry_stock = industry_group.get_group(sector)
            for stock in same_industry_stock.Symbol:
                if stock in df.columns and row[stock] != 0:
#                         print(2)
#                         row[stock]    
                    row[sector] = row[sector] + row[stock]
                    print(sector, idx)
                    df[sector][idx] = 999
                    print(df[sector][idx])
#                     df.loc[idx][sector] = 9999
#                     print()
#                     df.loc[idx].at['sector']=9999
#                     print(f"df[sector][idx] is {sector}, {idx}, the column is {df[sector]}")
#                     print(df[sector])
                    stock_num += 1
#             print(stock_num)
            if stock_num != 0:                    
                row[sector] = row[sector] / stock_num
#             print(stock_num)
#         print(df)
#         print(row)
    
#     df.to_csv('data/SP500_constituents_update.csv')
    
    return df


# In[24]:


df_sector['Health Care'][2] = 999


# In[25]:


df_sector


# In[30]:


df_clean = clean_stock_information(df)
df_sector = add_sector_y_datafile(df_clean, comp)


# In[ ]:


df_clean.loc[2]['AAL']


# In[ ]:


df_sector


# In[ ]:





# In[ ]:


if df_clean["AAL"][2]:
    print(1)


# In[ ]:


df_clean = clean_stock_information(df)
df_sector = add_sector_y_datafile(df_clean, comp)


# In[ ]:


df_sector


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


# def clean_stock_info(df, one_day):
#     """
#     """
#     # drop repetitive col
#     dropcolumn = []
#     if not one_day:
#         for name in df.columns:
#             if not (re.match(r"Adj Close.*", name) or name == "Attributes"):
#                 dropcolumn.append(name)
#     else:
#         for name in df.columns:
#             if (not 'Adj Close' in name) and (not "Date" in name):
#                 dropcolumn.append(name)

#     df = df.drop(columns = dropcolumn)
# #     print(df)
#     # format the csv file
#     if not one_day:
#         new_header = df.iloc[0] #grab the first row for the header
#         df = df[1:] #take the data less the header row
#         df.columns = new_header #set the header row as the df header
#         df.rename(columns={'Symbols':'Date'}, inplace=True)
#         df = df.drop(index=1)
        
#         for i, row in df.iterrows():
#             original_text = row["Date"].replace("-", "/")
#             print(original_text)
# #             new_text = original_text[5:] + "/" + original_text[:4]
# #             row["Date"] = new_text
        
#     else:
#         df.columns = [b for a, b in df.columns]
#         df.reset_index(inplace=True)
#         for i, row in df.iterrows():
#             row['Date']= row['Date'].strftime('%d/%m/%y')
#             original_text = row["Date"].str.replace("-", "/")
#             new_text = original_text[3:6] + original_text[:3] + "20" + original_text[6:]
#             row["Date"] = str(new_text)
#     df["Date"] = df["Date"].astype(dtype = str)
#     df["Date"] = df["Date"].str.replace("-", "/")
#     df = df.iloc[::-1]
#     return df


# In[ ]:


def add_sector_y_data(df, sp500, industry):
    """
    """

    sp500.set_index("Date", inplace = True)
    df.set_index("Date", inplace = True)
    combine = sp500.join(df)
    
    ######################### (check the number before submit) ######################
    # combine.drop(combine.tail(1).index,inplace=True) # delete the NA rows 
    combine.drop(combine.head(5).index,inplace=True) 
    # delete the NA columns
    combine = combine.dropna(axis = "columns") 
    
    # prepare industry data
#     industry = pd.read_csv('data/constituents.csv')
    for idx, row in industry.iterrows():
        row["Symbol"] = row["Symbol"].replace(".", "-")
        
    # add sector data
    industry_group = industry.groupby('Sector')
    for sector in industry.Sector.unique():
        stock_num = 0
        same_industry_stock = industry_group.get_group(sector)
        combine[sector] = 0
        for stock in same_industry_stock.Symbol:
            if stock in combine.columns:
                combine[stock] = combine[stock].astype(float)
                combine[sector] = combine[sector] + combine[stock]
                stock_num += 1
        combine[sector] = combine[sector] / stock_num
    
    combine.to_csv('data/SP500_constituents_update.csv')
    
    return

