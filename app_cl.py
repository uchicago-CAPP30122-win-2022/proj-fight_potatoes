import dash
import dash_html_components as html
import plotly.graph_objects as go
from dash import dcc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output


app = dash.Dash()
'''
# df1
df = pd.read_csv('test.csv', header = 0, thousands=',')
df['change'] = 100 * (df['Close*'] - df['Open'])/df['Open']

# df2
lst = ['High', 'Low', 'Close*', 'change']
df_mean = pd.DataFrame()
for var in lst:
    df_mean[var] = df.groupby('Date')[var].mean()
'''
df = pd.read_csv('fake_output.csv')

app.layout = html.Div([
        html.Div([
            html.H1("SOME TITLE"),
            html.P("ABOUT PARAGRAPH")
                ], 
            style = {'padding' : '50px' , 'backgroundColor' : '#3aaab2'}),


        html.Div([
            html.Label("Choose a model "),
            dcc.Dropdown(id = 'model_dropdown',
            options = [
                #{'label':'High', 'value':'High' },
                #{'label': 'Low', 'value':'Low'},
                #{'label': 'Close', 'value':'Close*'},
                #{'label': 'Change', 'value':'change'}
                {'label':'Linear Regression', 'value':'linear' },
                {'label': 'Logistic Regression', 'value':'logit'},
                ],
            value = 'linear')], style = {'width': '20%', 'display': 'inline-block'} ),
        html.Div([
            html.Label("Choose a sector "),
            dcc.Dropdown(id = 'sector_dropdown',
            options = [
                #{'label':'Apple', 'value':'AAPL' },
                #{'label': 'Google', 'value':'GOOGL'},
                #{'label': 'Lululemon', 'value':'LULU'},
                #{'label': 'Tesla', 'value':'TSLA'}
                {'label':'Information Technology', 'value':'Information Technology' },
                {'label': 'Financials', 'value':'Financials'},
                ],
            value = 'Financials')], style = {'width': "20%", 'display': 'inline-block'}),

        dcc.Graph(id = 'bar_plot')
])
    
    
@app.callback(Output(component_id='bar_plot', component_property= 'figure'),
              [Input(component_id='model_dropdown', component_property= 'value'),
              Input(component_id='sector_dropdown', component_property= 'value')])

def graph_update(model_value, sector_value):
    df1 = df[(df['industry'] == sector_value) & (df['model'] == model_value)]
    fig = go.Figure(go.Scatter(x = df1['date'], y = df1['actual'], 
                    name = 'Actual price using {} model'.format(model_value),
                    line = dict(color = 'firebrick', width = 4)))

    fig.add_trace(go.Scatter(x = df1['date'], y = df1['predicted'],
                    name = 'Predicted price {} model'.format(model_value),
                    line = dict(color = 'blue', width = 2, dash = 'dash')))
    
    fig.update_layout(title = 'Actual vs. Predicted for {}'.format(sector_value),
                      xaxis_title = 'Date',
                      yaxis_title = 'Price'
                      )

    '''                 
    fig = go.Figure([go.Scatter(x = df1['Date'], y = df1['{}'.format(dropdown_value)],
                     line = dict(color = 'firebrick', width = 4))
                     ])
    
    fig.update_layout(title = 'Stock prices over time',
                      xaxis_title = 'Dates',
                      yaxis_title = 'Prices'
                      )
    '''
    return fig



if __name__ == '__main__': 
    app.run_server()

