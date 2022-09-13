import pandas as pd
import numpy as np
import dash
from dash import dcc, html
from dash.dependencies import Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas_datareader as web
import time as tm
import datetime as dt
import plotly.graph_objects as go

data = pd.read_csv('data.csv')
categories = data['Source']

fig = go.Figure()

fig.add_trace(go.Scatterpolar(
      r=data['ESG-Avaliable'],
      theta=categories,
      fill='toself',
      name='ESG-Data'
))
fig.add_trace(go.Scatterpolar(
      r=data['SDG-Avaliable'],
      theta=categories,
      fill='toself',
      name='SDG-Data'
))
fig.add_trace(go.Scatterpolar(
      r=data['Sentiment-Avaliable'],
      theta=categories,
      fill='toself',
      name='Sentiment-Data'
))
radar = fig.update_layout(
  polar=dict(
    radialaxis=dict(
      visible=True,
      range=[13000, 17000]
    )),
  showlegend=False
)

means = pd.read_csv('ESGMean.csv')
std = pd.read_csv('std.csv')

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SPACELAB],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}])
server = app.server

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("2019-2020 ESG,SDG,Sentiment",
                        className='text-center text-primary, mb-3'),
                width=12)
    ]),
    dbc.Row([
        dbc.Col([
            html.P('Select Data Type:',
                   style={'textDecoration': 'underline'}),
            dcc.Checklist(id='checklist', value=['ESG-Mean'],
                          options=['ESG-Mean','SDG-Mean','Sentiment-Mean'],
                          labelClassName='mr-3 text-success'),
            dcc.Graph(id='line-fig', figure={})
        ], width={'size': 12}),
        ]),
    dbc.Row([
        dbc.Col([
            html.P('Select Data Type:',
                   style={'textDecoration': 'underline'}),
            dcc.Checklist(id='checklist1', value=['ESG-STD'],
                          options=['ESG-STD','SDG-STD','Sentiment-STD'],
                          labelClassName='mr-3 text-success'),
            dcc.Graph(id='line-fig1', figure={})
        ], width={'size': 12}),
        ]),
    dbc.Row([
        dbc.Col([
            html.P('Data Gap'),
            dcc.Graph(id='line-fig2', figure=radar)]
        , width={'size': 12},
        )
])
])
@app.callback(
    Output('line-fig', 'figure'),
    Input('checklist', 'value')
)
def update_graph(stock_slctd):
    means1 = means[means['Type'].isin(stock_slctd)]
    figln2 = px.line(means1, x='Timestamps', y='Mean', color='Type')
    return figln2

@app.callback(
    Output('line-fig1', 'figure'),
    Input('checklist1', 'value')
)
def update_graph(stock_slctd):
    stdd = std[std['Type1'].isin(stock_slctd)]
    figln2 = px.line(stdd, x='Timestamps', y='Data1', color='Type1')
    return figln2



if __name__ == '__main__':
    app.run_server(debug=True, port=8000)
