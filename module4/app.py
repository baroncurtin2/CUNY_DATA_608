import dash
import dash_core_components as dcc
import dash_html_components as html

from nyc_opendata import OpenData

# data source
nyc = OpenData()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='New York City Tree Census'),

    html.Div(children="Tree Health by Borough"),

    html.Div(children=[
        html.Label('Borough'),
        dcc.Dropdown(options=nyc['borough'],
            value=nyc['borough'][0]),

        html.Label('Health'),
        dcc.Dropdown(options=nyc['health'],
                     value=nyc['health'][0]),

        html.Label('Species'),
        dcc.Dropdown(options=nyc['species'],
                     value=nyc['species'][0]),

        html.Label('Steward'),
        dcc.Dropdown(options=nyc['steward'],
                     value=nyc['steward'][0]),
    ], style={'columnCount': 2})
])

if __name__ == '__main__':
    app.run_server(debug=True)
