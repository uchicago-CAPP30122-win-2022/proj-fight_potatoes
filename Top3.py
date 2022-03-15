#!/usr/bin/env python
# coding: utf-8

# In[24]:


import pandas as pd

import csv


# In[25]:



df = pd.read_csv('/Users/siwenchen/Desktop/proj-fight_potatoes-master/test_output.csv')


# In[26]:


def each_model(df,model_name):
    '''
    Input: a model name 
    
    Output: a list of top 3 sectors
    
    
    '''
    result= df[df["model"] == model_name].sort_values(by=["R2"],ascending=False).head(6)
    top_3 = []
    for i in result["sector"]:
        if i not in top_3:
            top_3.append("  ")
            top_3.append(i)
            top_3.append("/")
    return top_3


# In[27]:


def GetTheTopThreeSectors(df):
    '''
    This function collect a pandas dataframe.
    For each topic(china/covid),
    we will get the top 3 sectors that have the highest 
    R-square under different model
    
    Input:a pandas dataframe
    Output: a pandas dataframe shows the top 3 sectors with the topic and model
    
    '''
    # List 1
    topic = ['China','China','China','China',"Covid","Covid","Covid","Covid"]
    
    # List 2
    classifer = ['Linear','Logit','KNN','SVMLinear','Linear','Logit','KNN','SVMLinear']
    
    #list 3 
    
    top_3_sectors = []
    df = df[df["sector"] != "All Sectors"]
    china_df = df[df["topic"] == "china"]
    
        
    top_3_sectors.append(tuple(each_model(china_df,"linear")))
    
    top_3_sectors.append(tuple(each_model(china_df,"logistic")))
            
    top_3_sectors.append(tuple(each_model(china_df,"KNN")))
    
    top_3_sectors.append(tuple(each_model(china_df,"SVM")))

    covid_df = df[df["topic"] == "covid"]   
    
    top_3_sectors.append(tuple(each_model(covid_df,"linear")))
    
    top_3_sectors.append(tuple(each_model(covid_df,"logistic")))
            
    top_3_sectors.append(tuple(each_model(covid_df,"KNN")))
    
    top_3_sectors.append(tuple(each_model(covid_df,"SVM")))
    
    
    # and merge them by using zip().  
    list_tuples = list(zip(topic, classifer,top_3_sectors)) 
    new_list_tuples = '  '.join(str(list_tuples))
    
    # Converting lists of tuples into pandas Dataframe.  
    dframe = pd.DataFrame(list_tuples, columns=['topic', 'classifier',"top 3 sectors"])  
    
    return dframe


# In[28]:


GetTheTopThreeSectors(df)


# In[ ]:


import dash_html_components as html
from dash import Dash, dash_table
import pandas as pd

result = GetTheTopThreeSectors(df)

app = Dash(__name__)

app.layout = html.Div([
html.H1("Accuracy of each classifier per sector — Top 5", style={'textAlign': 'center', 'color': '#7FDBFF'}),
dash_table.DataTable(result.to_dict('records'), [{"name": i, "id": i} for i in result.columns])])


if __name__ == '__main__':
    app.run_server()


# In[ ]:





# In[ ]:




