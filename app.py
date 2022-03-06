import dash
import dash_html_components as html
import plotly.graph_objects as go
from dash import dcc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output


app = dash.Dash()

df = pd.read_csv('test.csv', header = 0, thousands=',')
df['date'] = pd.to_datetime(df['Date'])
df['date'] = df['date'].dt.date
df['change'] = 100 * (df['Close*'] - df['Open'])/df['Open']


app.layout = html.Div([
        html.Div([
            html.H1("SOME TITLE"),
            html.P("ABOUT PARAGRAPH")
                ], 
            style = {'padding' : '50px' , 'backgroundColor' : '#3aaab2'}),
        dcc.Graph(id = 'bar_plot'),

        html.P([
            html.Label("Choose a feature"),
            dcc.Dropdown(id = 'dropdown',
            options = [
                {'label':'High', 'value':'High' },
                {'label': 'Low', 'value':'Low'},
                {'label': 'Close', 'value':'Close*'},
                {'label': 'Change', 'value':'change'}
                ],
            value = 'High')]),
        html.P([
            html.Label("Choose a company"),
            dcc.Dropdown(id = 'co_dropdown',
            options = [
                {'label':'Apple', 'value':'AAPL' },
                {'label': 'Google', 'value':'GOOGL'},
                {'label': 'Lululemon', 'value':'LULU*'},
                {'label': 'Tesla', 'value':'TSLA'}
                ],
            value = 'AAPL')])
])
    
    
@app.callback(Output(component_id='bar_plot', component_property= 'figure'),
              [Input(component_id='dropdown', component_property= 'value'),
              Input(component_id='co_dropdown', component_property= 'value')])
def graph_update(dropdown_value, company_value):
    df1 = df[df['ticker'] == company_value]
    fig = go.Figure([go.Scatter(x = df1['Date'], y = df1['{}'.format(dropdown_value)],
                     line = dict(color = 'firebrick', width = 4))
                     ])
    
    fig.update_layout(title = 'Stock prices over time',
                      xaxis_title = 'Dates',
                      yaxis_title = 'Prices'
                      )
    return fig  



if __name__ == '__main__': 
    app.run_server()

