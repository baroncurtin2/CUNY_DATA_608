import pandas as pd


def get_data():
    url = 'https://data.cityofnewyork.us/resource/nwxe-4ae8.json'
    trees = pd.read_json(url)
    return trees
