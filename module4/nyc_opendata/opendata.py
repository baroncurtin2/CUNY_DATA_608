import pandas as pd
import numpy as np


class OpenData:
    def __init__(self):
        self.__url = 'https://data.cityofnewyork.us/resource/nwxe-4ae8.json?'
        self.data = self.__get_data()
        self.unique_lists = self.__get_uniques()

    def __query_maker(self, limit=10000, offset=0):
        query = self.__url + \
                '$select=boroname AS borough,spc_common AS species,health,steward,count(tree_id) AS trees' + \
                '&$group=boroname,spc_common,health,steward' + \
                '&$order=boroname,spc_common,health,steward' + \
                f'&$limit={limit}' + \
                f'&$offset={offset}'
        query = query.replace(' ', '%20')
        return query

    def __get_query_results(self, query):
        result = pd.read_json(query)
        return result

    def __get_data(self):
        offset = 0
        limit = 10000
        chunk = 10000
        dfs = []

        while True:
            query = self.__query_maker(limit=limit, offset=offset)
            result = self.__get_query_results(query)
            dfs.append(result)
            offset += chunk

            # end loop when result is less than chunksize
            if len(dfs[-1]) < chunk:
                break

        return pd.concat(dfs)

    def __get_uniques(self):
        only_obs = self.data.select_dtypes(include='object')
        uniques = {col: [{'label': option, 'value': option} for option in sorted(only_obs[col].dropna().unique())]
                   for col in only_obs.columns}
        return uniques
