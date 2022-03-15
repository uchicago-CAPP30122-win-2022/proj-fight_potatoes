#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from dash import Dash, dash_table
import pandas as pd

df = pd.read_csv("test_data - Sheet1.csv")

app = Dash(__name__)

app.layout = html.Div([
html.H1("Accuracy of each classifier per sector — Top 5", style={'textAlign': 'center', 'color': '#7FDBFF'}),
dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns])])

if __name__ == '__main__':
    app.run_server()

