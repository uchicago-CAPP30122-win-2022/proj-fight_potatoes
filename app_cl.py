import dash
import dash_html_components as html
import plotly.graph_objects as go
from dash import dcc
import plotly.express as px
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output


app = dash.Dash()

all_options = {
    'linear': ['Information Technology', 'Financials'],
    'logit': ['All Sectors'],
    'knn': ['All Sectors'],
    'svm': ['All Sectors']
}

df = pd.read_csv('fake_output.csv')
tr = pd.read_csv('fake_training_output.csv')

tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px'
}

app.layout = html.Div([
        html.Div([
            html.H1("Can Moods on Twitter Predict Stock Price Movements?"),
            #html.P('Stock prices are often influenced by the public attitude '
            #    'towards the market. Psychological research shows that emotions play a '
            #    'significant role in human decision-making. Similarly, behavioral finance research '
            #    "shows that financial decisions are influenced by people's emotions and moods. "),
            #html.P("Twitter is a popular place for users to express their moods and sentiments "
            #    "towards a variety of topics. We looked into how the polarity of "
            #    "sentiments in tweets on COVID-19 and US-China relations are related to "
            #    "the daily movements of stock prices!") 
                ], 
            style = {'padding' : '10px' , 'backgroundColor' : '#3aaab2'}),

        html.Div([
            html.Label("Choose a topic "),
            dcc.Dropdown(id = 'topic_dropdown',
            options = [
                {'label':'US-China Relations', 'value':'China' },
                {'label': 'COVID-19', 'value':'covid'},
                ],
            value = 'covid')], style = {'padding': '5px', 'width': '20%', 'display': 'inline-block'} ),

        html.Div([
            html.Label("Choose a model "),
            dcc.Dropdown(id = 'model_dropdown',
            options = [
                {'label':'Linear Regression', 'value':'linear' },
                {'label': 'Logistic Regression', 'value':'logit'},
                ],
            value = 'linear')], style = {'padding': '5px', 'width': '20%', 'display': 'inline-block'} ),

        html.Div([
            html.Label("Choose a sector "),
            dcc.Dropdown(id='sector_dropdown', options=[])], 
            style = {'padding': '5px', 'width': "20%", 'display': 'inline-block'}),

        html.H3('Testing the model', style = {'padding': '3px'}),
        dcc.Graph(id = 'bar_plot'),

        html.H3('Model fit for the training data', style = {'padding': '3px'}),
        dcc.Graph(id = 'training_plot'),

        #dcc.Tabs(id='tabs', value='tabs', parent_className='custom-tabs', children=[
        #    dcc.Tab(
        #            label='Tweets ',
        #            value='tweets', className = 'control-tabs',
        #            style={'width': '30%','padding': '3px', 'fontSize': '18px',
        #            'line-height': '5vh'}),

        #    dcc.Tab(
        #            label='The Stock Data',
        #            value='stock', className = 'control-tabs',
        #           style={'width': '30%','padding': '3px', 'fontSize': '18px',
        #            'line-height': '5vh'}),
        #       ]),

        dcc.Tabs(id="tabs-styled-with-inline", value='tab-1', children=[
            dcc.Tab(label='About', value='About', style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(label='The Tweet Data', value='The Tweet Data', style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(label='The Stock Data', value='The Stock Data', style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(label='The Output', value='The Output', style=tab_style, selected_style=tab_selected_style),
        ], style=tabs_styles), 
    html.Div(id='tabs-content-inline')


])
    
@app.callback(
    Output('sector_dropdown', 'options'),
    Input('model_dropdown', 'value')
)
def set_sector_options(model):
    return [{'label': c, 'value': c} for c in all_options[model]]

@app.callback(
    Output('sector_dropdown', 'value'),
    Input('sector_dropdown', 'options'))
def set_sector_value(available_options):
    return available_options[0]['value']


@app.callback(Output('bar_plot', 'figure'),
            [Input('topic_dropdown', 'value'),
            Input('model_dropdown', 'value'),
            Input('sector_dropdown', 'value')])

def graph_update(topic, model_value, sector_value):
    if model_value == 'linear':
        df1 = df[(df['topic'] == topic) & (df['industry'] == sector_value) & (df['model'] == model_value)]
        fig = go.Figure(go.Scatter(x = df1['date'], y = df1['actual'], 
                        name = 'Actual price using {} model'.format(model_value),
                        line = {'color': 'firebrick', 'width': 4}))

        fig.add_trace(go.Scatter(x = df1['date'], y = df1['predicted'],
                        name = 'Predicted price {} model'.format(model_value),
                        line = {'color': 'blue', 'width': 2, 'dash': 'dash'}))
        
        fig.update_layout(title = 'Actual vs. Predicted for {} Sector'.format(sector_value),
                        xaxis_title = 'Date',
                        yaxis_title = 'Price'
                        )
    else:
        df1 = df[(df['topic'] == topic) & (df['model'] == model_value)]
        df1['accurate'] = np.where(df1['predicted'] == df1['actual'], 1, 0)
        df2 = pd.DataFrame()
        df2['accuracy'] = df1.groupby('industry')['accurate'].mean()
        df2.reset_index(inplace = True)

        fig = go.Figure(go.Bar(x = df2['industry'], y = df2['accuracy']
                        ))
        fig.update_layout(title = 'Accuracy rate using {} model'.format(model_value),
                        xaxis_title = 'Sector',
                        yaxis_title = 'Accuracy rate (%)'
                        )

    return fig

'''
@app.callback(Output('tabs-content-classes', 'children'),
            Input('tabs', 'value'))
def render_content(tab):
    if tab == 'stock':
        return html.Div([
            html.P(
                "We collected stock data from all S&P 500 companies and grouped the data "
                "into 11 different sectors: Information Technology, Health Care, Consumer "
                "Discretionary, Financials, Communication Services, Industrials, Consumer Staples, "
                "Energy, Real Estate, Materials, and Utilities.", style = {'fontSize': "16px"} )
        ])
    elif tab == 'tweets':
        return html.Div([
            html.P(
                "Tweets were collected from the Twitter Developer API. "
                "We gathered XXXX tweets related to COVID-19 and "
                "US-China Relations from DATE1 to DATE2. "),
            html.P(
                'The query keywords used to collect tweets are as follows: '),
            html.P(
                'COVID-19: covid19, covid, covid-19, vaccine, vaccination, omicron, '
                'booster, mask, mandate, lockdown, death rate, travel restriction, '
                'total infections, breakthrough infections, social distancing, '
                'quarantine, isolation, pandemic, & shutdown. '),
            html.P(
                'US-China Relations: Trump, Biden, trade war, Xi Jinping, Eileen Gu, '
                'Taiwan, Hong Kong, CCP, TikTok, Huawei, tariffs, human rights, '
                'Xinjiang, Zhao Lijian, & Ned Price.'
            ), 
        ])
'''
@app.callback(Output('tabs-content-inline', 'children'),
              Input('tabs-styled-with-inline', 'value'))
def render_content(tab):
    if tab == 'About':
        return html.Div([
            html.H3("""
            Stock prices are influenced by the public attitude towards 
            the market. Psychological research that emotions play a significant role 
            in human decision-making. Behavioral finance showed that financial decisions 
            are influenced by people's emotions and moods. """),
            html.H3('''
            Twitter is a popular place for users to express their moods and sentiments 
            towards a variety of topics. We look into how the polarity of sentiments in 
            tweets is related to the daily movements of stock prices!
            ''')
        ])
    elif tab == 'The Tweet Data':
        return html.Div([
                    html.H3('''
                        Tweets were collected from the Twitter Developer API. 
                        We gathered XXXX tweets related to COVID-19 and 
                        US-China Relations from DATE1 to DATE2. 
                        '''),
                    html.H3(
                        'The query keywords used to collect tweets are as follows: '),
                    html.H3('''
                        COVID-19: covid19, covid, covid-19, vaccine, vaccination, omicron,
                        booster, mask, mandate, lockdown, death rate, travel restriction,
                        total infections, breakthrough infections, social distancing,
                        quarantine, isolation, pandemic, & shutdown. '''),
                    html.H3(
                        'US-China Relations: Trump, Biden, trade war, Xi Jinping, Eileen Gu, '
                        'Taiwan, Hong Kong, CCP, TikTok, Huawei, tariffs, human rights, '
                        'Xinjiang, Zhao Lijian, & Ned Price.'
            ), 
        ])
    elif tab == 'The Stock Data':
        return html.Div([
            html.H3('''
                We collected stock data from all S&P 500 companies and grouped the data 
                into 11 different sectors: Information Technology, Health Care, Consumer 
                Discretionary, Financials, Communication Services, Industrials, Consumer Staples, 
                Energy, Real Estate, Materials, and Utilities.
            '''
            )
        ])
    elif tab == 'The Output':
        return html.Div([
            html.H3('''
            You can check out the differences through the various dropdown menus. 
            For both topics, you may select
            a model to see the accuracy of the prediction using average Twitter
            sentiments on stock market movement. 
            If you choose linear regression, you can choose a sector.
            For all other models, we show the accuracy of the models with all sectors
            on one plot.
            '''
            )
        ])

@app.callback(Output('training_plot', 'figure'),
            [Input('topic_dropdown', 'value'),
            Input('model_dropdown', 'value'),
            Input('sector_dropdown', 'value')])
def graph_update_tr(topic, model_value, sector_value):
    if model_value == 'linear':
        tr1 = tr[(tr['topic'] == topic) & (tr['industry'] == sector_value) & (tr['model'] == model_value)]
        fig1 = go.Figure(go.Scatter(x = tr1['date'], y = tr1['true_y'], 
                        name = 'Actual price using {} model'.format(model_value),
                        line = {'color': 'firebrick', 'width': 4}))

        fig1.add_trace(go.Scatter(x = tr1['date'], y = tr1['fitted_y'],
                        name = 'Fitted price {} model'.format(model_value),
                        line = {'color': 'blue', 'width': 2, 'dash': 'dash'}))
        
        fig1.update_layout(title = 'Actual vs. Fitted for {} Sector'.format(sector_value),
                        xaxis_title = 'Date',
                        yaxis_title = 'Price'
                        )
    else:
        tr1 = tr[(tr['topic'] == topic) & (tr['model'] == model_value)]
        tr1['accurate'] = np.where(tr1['fitted_y'] == tr1['true_y'], 1, 0)
        tr2 = pd.DataFrame()
        tr2['accuracy'] = tr1.groupby('industry')['accurate'].mean()
        tr2.reset_index(inplace = True)

        fig1 = go.Figure(go.Bar(x = tr2['industry'], y = tr2['accuracy']
                        ))
        fig1.update_layout(title = 'Training accuracy rate using {} model'.format(model_value),
                        xaxis_title = 'Sector',
                        yaxis_title = 'Accuracy rate (%)'
                        )

    return fig1

if __name__ == '__main__': 
    app.run_server()
