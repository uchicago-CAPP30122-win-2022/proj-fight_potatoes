#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from dash import Dash, dcc, html

from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

tab_height = '5vh'
app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Tabs(id="tabs", value='tab-1', style={
        'width': '50%',
        'font-size': '200%',
        'height':tab_height
    },
             
    children=[
        dcc.Tab(label='The tweet data', value='tab-1', style={'width': '50%','padding': '0','line-height': tab_height},selected_style={'padding': '0','line-height': tab_height}),
        dcc.Tab(label='The stock data', value='tab-2',style={'width': '50%','padding': '0','line-height': tab_height},selected_style={'padding': '0','line-height': tab_height}),
    ]),
    html.Div(id='tabs-content')
])

@app.callback(Output('tabs-content', 'children'),
              Input('tabs', 'value'))
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            html.H3(r"""The tweet data was gathered by “scraping” Twitter using its Developer API. We gathered XXXX amount of tweets related to the COVID and the US-China Relationship since these two topics were hotly discussed among Twitter users.
            
            COVID:Vaccination/Omicron/Booster/mask/Lockdown/Covid-19/Death rate/Covid test/Travel restriction/Positivity rates/total infections/Mandate/Breakthrough infections/Social distancing/Quarantine/Isolation/Pandemic/Shutdown\US-CHINA RELATIONS
            
            US-China Relations/Xi Jinping/Trump/Trade war/Xinjiang/Biden/Eileen Gu/Taiwan/Hong Kong/CCP/TikTok/Huawei/Tariffs/Human rights.""")
    
        ])
    elif tab == 'tab-2':
        return html.Div([
            html.H3('The financial data we are using are S&P 500 data and showed the difference among different sectors including Health care, Consumer discretionary, Financials, Communication Services, Industrials, Consumer Staples, Energy, Real estate, Materials, Utilities.')
        ])


if __name__ == '__main__':
    app.run_server()


# In[ ]:





# In[ ]:





# In[ ]:




