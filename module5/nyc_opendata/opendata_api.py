from flask import Flask, jsonify, send_from_directory, render_template
import pandas as pd

app = Flask(__name__)


@app.route('/opendata/<string:borough>')
def return_tree_data(borough):
    url = 'https://data.cityofnewyork.us/resource/nwxe-4ae8.json?'

    def query_maker(limit=10000, offset=0):
        query = (url +
                 '$select=boroname AS borough,health,count(tree_id) AS trees' +
                 f'&$where=boroname="{borough}"' +
                 '&$group=boroname,health' +
                 '&$order=boroname,health' +
                 f'&$limit={limit}' +
                 f'&$offset={offset}')
        query = query.replace(' ', '%20')
        return query

    def get_data():
        offset = 0
        limit = 10000
        chunk = 10000
        dfs = []

        while True:
            query = query_maker(limit=limit, offset=offset)
            result = pd.read_json(query)
            dfs.append(result)
            offset += chunk

            # end loop when result is less than chunksize
            if len(dfs[-1]) < chunk:
                break

        return pd.concat(dfs)

    data = get_data()
    html_table = data[['health', 'trees']].to_html(classes='data', header='true')
    return render_template('subpage.html', borough=borough, tables=[html_table])


# index.html
@app.route('/')
def index():
    return render_template('index.html')


# load local javascript
@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', 'path')


if __name__ == '__main__':
    app.run(debug=True)
