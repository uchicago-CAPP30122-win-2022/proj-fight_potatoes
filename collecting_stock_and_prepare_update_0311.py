#!/usr/bin/env python
# coding: utf-8

# In[276]:


import pandas as pd
import pandas_datareader as web


# In[277]:


comp = pd.read_csv("data/constituents.csv")
comp_lst = pd.Series(comp['Symbol']).str.replace(".", '-')
comp_lst = list(comp_lst)


# In[ ]:


df = web.DataReader(comp_lst, 'yahoo', '2/14/22', '3/11/22')


# In[266]:


# df = pd.read_csv('data/SP500_constituents.csv')


# In[ ]:


# drop repetitive col
dropcolumn = []
for name in df.columns:
    if not (re.match(r"Adj Close.*", name) or name == "Attributes"):
        dropcolumn.append(name)
        
df = df.drop(columns = dropcolumn)


# In[ ]:


# format the csv file
new_header = df.iloc[0] #grab the first row for the header
df = df[1:] #take the data less the header row
df.columns = new_header #set the header row as the df header
df.rename(columns={'Symbols':'Date'}, inplace=True)
df = df.drop(index=1)

for i, row in df.iterrows():
    original_text = row["Date"].replace("-", "/")
    new_text = original_text[5:] + "/" + original_text[:4]
    row["Date"] = new_text
    
df = df.iloc[::-1] 


# In[ ]:


# combine s&p 500 files with stock files
sp500 = pd.read_csv('data/S&P_update.csv')
sp500.set_index("Date", inplace = True)
df.set_index("Date", inplace = True)
combine = sp500.join(df)


# In[ ]:


######################### (check the number before submit) ######################
combine.drop(combine.tail(7).index,inplace=True) # delete the NA rows 
combine.dropna(axis = "columns") # delete the NA columns


# In[ ]:


# prepare industry data
industry = pd.read_csv('data/constituents.csv')
for idx, row in industry.iterrows():
    row["Symbol"] = row["Symbol"].replace(".", "-")


# In[ ]:


# add sector data
industry_group = industry.groupby('Sector')
for sector in industry.Sector.unique():
    same_industry_stock = industry_group.get_group(sector)
    combine[sector] = 0
    for stock in same_industry_stock.Symbol:
        combine[stock] = combine[stock].astype(float)
        combine[sector] = combine[sector] + combine[stock]


# In[ ]:


combine.to_csv('data/SP500_constituents_update.csv')


# In[ ]:


# CHECK WHETHER NA????????????????


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





# In[15]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[72]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




