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
    'logit': ['All industries']
}

df = pd.read_csv('fake_output.csv')

app.layout = html.Div([
        html.Div([
            html.H1("SOME TITLE"),
            html.P("ABOUT PARAGRAPH")
                ], 
            style = {'padding' : '50px' , 'backgroundColor' : '#3aaab2'}),

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

        dcc.Graph(id = 'bar_plot')
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


@app.callback(Output(component_id='bar_plot', component_property= 'figure'),
            [Input(component_id='topic_dropdown', component_property= 'value'),
            Input(component_id='model_dropdown', component_property= 'value'),
            Input(component_id='sector_dropdown', component_property= 'value')])

def graph_update(topic, model_value, sector_value):
    if model_value == 'linear':
        df1 = df[(df['topic'] == topic) & (df['industry'] == sector_value) & (df['model'] == model_value)]
        fig = go.Figure(go.Scatter(x = df1['date'], y = df1['actual'], 
                        name = 'Actual price using {} model'.format(model_value),
                        line = dict(color = 'firebrick', width = 4)))

        fig.add_trace(go.Scatter(x = df1['date'], y = df1['predicted'],
                        name = 'Predicted price {} model'.format(model_value),
                        line = dict(color = 'blue', width = 2, dash = 'dash')))
        
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


if __name__ == '__main__': 
    app.run_server()
