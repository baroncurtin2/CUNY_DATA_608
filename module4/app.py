import dash
import dash_core_components as dcc
import dash_html_components as html

from nyc_opendata import OpenData

# data source
nyc = OpenData()
data = nyc.data
lists = nyc.unique_lists
print(nyc.unique_lists)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='New York City Tree Census'),

    html.Div(children="Tree Health by Borough"),

    html.Div(children=[
        html.Label('Borough'),
        dcc.Dropdown(options=lists['borough'],
                     value=lists['borough'][0]),

        html.Label('Health'),
        dcc.Dropdown(options=lists['health'],
                     value=lists['health'][0]),

        html.Label('Species'),
        dcc.Dropdown(options=lists['species'],
                     value=lists['species'][0]),

        html.Label('Steward'),
        dcc.Dropdown(options=lists['steward'],
                     value=lists['steward'][0]),
    ], style={'columnCount': 2})
])

if __name__ == '__main__':
    app.run_server(debug=True)
