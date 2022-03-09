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
    'logit': ['All Sectors']
}

df = pd.read_csv('fake_output.csv')

app.layout = html.Div([
        html.Div([
            html.H1("Can Moods on Twitter Predict Stock Price Movements?"),
            #html.P("ABOUT PARAGRAPH")
                ], 
            style = {'padding' : '30px' , 'backgroundColor' : '#3aaab2'}),

        html.Div([
            html.Label("Choose a topic "),
            dcc.Dropdown(id = 'topic_dropdown',
            options = [
                {'label':'US-China Relations', 'value':'China' },
                {'label': 'COVID-19', 'value':'covid'},
                ],
            value = 'covid')], style = {'width': '20%', 'display': 'inline-block'} ),

        html.Div([
            html.Label("Choose a model "),
            dcc.Dropdown(id = 'model_dropdown',
            options = [
                {'label':'Linear Regression', 'value':'linear' },
                {'label': 'Logistic Regression', 'value':'logit'},
                ],
            value = 'linear')], style = {'width': '20%', 'display': 'inline-block'} ),

        html.Div([
            html.Label("Choose a sector "),
            dcc.Dropdown(id='sector_dropdown', options=[])], 
            style = {'width': "20%", 'display': 'inline-block'}),

        dcc.Graph(id = 'bar_plot'),

        dcc.Tabs(id='tabs', value='tabs', parent_className='custom-tabs', children=[
            dcc.Tab(
                    label='About',
                    value='what-is', className = 'control-tabs'),

            dcc.Tab(
                    label='Data',
                    value='data', className = 'control-tabs'),
                ]),
        html.Div(id='tabs-content-classes')
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


@app.callback(Output('tabs-content-classes', 'children'),
              Input('tabs', 'value'))
def render_content(tab):
    if tab == 'what-is':
        return html.Div([
            html.P(
                'Stock prices are often influenced by the public attitude '
                'towards the market. Psychological research shows that emotions play a '
                'significant role in human decision-making. Similarly, behavioral finance research '
                "shows that financial decisions are influenced by people's emotions and moods."
            ),
            html.P(
                "Twitter is a popular place for users to express their moods and sentiments "
                "towards a variety of topics. We looked into how the polarity of "
                "sentiments in tweets on COVID-19 and US-China relations are related to "
                "the daily movements of stock prices!" )
        ])
    elif tab == 'data':
        return html.Div([
            html.P(
                "Tweets were collected from the Twitter Developer API. "
                "We gathered XXXX amount of tweets related to COVID-19 and "
                "US-China Relations from DATE1 to DATE2 "
            ),
            html.P(
                "We collected stock data from all S&P 500 companies and grouped the data "
                "into 11 different sectors: Health Care, Consumer Discretionary, "
                "Financials, Communication Services, Industrials, Consumer Staples, "
                "Energy, Real Estate, Materials, and Utilities." )
        ])
if __name__ == '__main__': 
    app.run_server()
