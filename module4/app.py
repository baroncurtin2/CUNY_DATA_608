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

# get initial set of data
pie_data = data.copy()
pie_data = pie_data[(pie_data['borough'] == boros[0]['value']) & (pie_data['species'] == species[0]['value'])]

# create dataset for percents
bar_data = data.copy()
bar_data = bar_data.groupby(['borough', 'species', 'steward', 'health']).sum()
bar_data = bar_data.groupby(level=[0, 1, 2]).apply(lambda x: x / x.sum()).reset_index()
bar_data = bar_data[(bar_data['borough'] == boros[0]['value']) & (bar_data['species'] == species[0]['value'])]

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
                          go.Pie(labels=pie_data['health'],
                                 values=pie_data['trees'])
                      ],
                      layout=go.Layout(
                          title='Tree Health by %'
                      )
                  )),
        dcc.Graph(id='bar-graph',
                  figure=go.Figure(
                      data=[go.Bar(
                          x=bar_data[(bar_data['health'] == health) & (bar_data['steward'] == steward)]['steward'],
                          y=round(bar_data[(bar_data['health'] == health) & (bar_data['steward'] == steward)]['trees'],
                                  2),
                          name=health,
                          text=round(bar_data[(bar_data['health'] == health) & (bar_data['steward'] == steward)][
                                         'trees'], 2),
                          textposition='auto'
                      )
                          for steward in bar_data['steward'].unique()
                          for health in bar_data['health'].unique()],
                      layout=go.Layout(
                          barmode='group',
                          title='Health Impact by Steward'
                      )
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
    # pie chart
    pie = data.copy()
    bar = data.copy()

    # filter bar and bar datasets for boro and spc
    pie = pie[(pie['borough'] == boro) & (pie['species'] == spc)]
    bar = bar.groupby(['borough', 'species', 'steward', 'health']).sum()
    bar = bar.groupby(level=[0, 1, 2]).apply(lambda x: x / x.sum()).reset_index()
    bar = bar[(bar['borough'] == boro) & (bar['species'] == spc)]

    # get pie and bar labels/values for easy referencing
    pie_labels = pie['health']
    pie_values = pie['trees']

    # pie graph items
    pie_trace = go.Pie(labels=pie_labels, values=pie_values)
    pie_fig = go.Figure(data=[pie_trace], layout=go.Layout(title='Tree Health by %'))

    # bar graph items
    bar_trace = [go.Bar(
        x=bar[(bar['health'] == health) & (bar['steward'] == steward)]['steward'],
        y=round(bar[(bar['health'] == health) & (bar['steward'] == steward)]['trees'], 2),
        name=health,
        text=round(bar[(bar['health'] == health) & (bar['steward'] == steward)]['trees'], 2),
        textposition='auto'
    )
        for steward in bar['steward'].unique()
        for health in bar['health'].unique()]
    bar_layout = go.Layout(barmode='group', title='Health Impact by Steward')
    bar_fig = go.Figure(data=bar_trace, layout=bar_layout)

    return pie_fig, bar_fig


if __name__ == '__main__':
    app.run_server(debug=True)
