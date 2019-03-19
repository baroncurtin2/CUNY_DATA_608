import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.plotly as py
import plotly.graph_objs as go

import pandas as pd
import numpy as np

from nyc_opendata import OpenData

# data source
nyc = OpenData()
data = nyc.data
lists = nyc.unique_lists
boros = lists['borough']
species = lists['species']

initial_data = data.pivot_table(values='trees', index=['borough', 'species', 'health'], aggfunc=np.sum)
initial_data = initial_data.reset_index().set_index(['borough', 'species']).loc[(
    boros[0]['value'], species[0]['value'])]

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='New York City Tree Census'),

    html.Div(children=[
        html.H5('Tree Health by Borough'),

        html.Div(children=[
            html.Label('Borough'),
            dcc.Dropdown(id='boro-filter',
                         options=lists['borough'],
                         value=lists['borough'][0]['value']),
            html.Label('Species'),
            dcc.Dropdown(id='spc-filter',
                         options=lists['species'],
                         value=lists['species'][0]['value'])
        ], style={'width': '50%'}),
    ]),

    html.Div(children=[
        dcc.Graph(id='pie-graph',
                  figure=go.Figure(
                      data=[
                          go.Pie(labels=initial_data['health'],
                                 values=initial_data['trees'])
                      ]
                  )),
        dcc.Graph(id='bar-graph',
                  figure=go.Figure(
                      data=[
                          go.Bar(x=initial_data['health'],
                                 y=initial_data['trees'])
                      ]
                  ))
    ], style={'columnCount': 2, 'width': '90%'})
])


@app.callback(
    [Output('pie-graph', 'figure'),
     Output('bar-graph', 'figure')],
    [Input('boro-filter', 'value'),
     Input('spc-filter', 'value')]
)
def update_graph(boro, spc):
    table = data.pivot_table(values='trees', index=['borough', 'species', 'health'], aggfunc=np.sum)
    print(spc)

    # reset and set index to borough for easier filtering
    table = table.reset_index().set_index(['borough', 'species'])

    # filter data for bor
    table = table.loc[(boro, spc)]
    labels = table['health']
    values = table['trees']

    # pie graph items
    pie_trace = go.Pie(labels=labels, values=values)
    pie_fig = go.Figure(data=[pie_trace])

    # bar graph items
    bar_trace = go.Bar(x=labels, y=values)
    bar_fig = go.Figure(data=[bar_trace])

    return pie_fig, bar_fig


if __name__ == '__main__':
    app.run_server(debug=True)
