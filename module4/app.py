import dash
import dash_core_components as dcc
import dash_html_components as html

from .nyc_opendata import get_data


# obtain df of trees data
df = get_data()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='New York City Tree Census')
])

if __name__ == '__main__':
    app.run_server(debug=True)
