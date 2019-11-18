import json
import logging

import pandas as pd
import requests

from .common import (
    HEADER, KSQL_SERVER_URL, LIST_TOPICS, LIST_STREAMS, LIST_TABLES, LIST_QUERIES, ENCODING,
    KSQL_OFFSET)

logger = logging.getLogger(__name__)


class REST(object):
    def __init__(
            self,
            base_url=KSQL_SERVER_URL
    ):
        self._base_url = base_url
        self._header = HEADER

    def get(self, path):
        response = requests.get(self._base_url + path)
        return response.json()

    def post(self, path, data):
        response = requests.post(self._base_url + path, headers=self._header, data=json.dumps(data))
        return response

    def get_status(self):
        '''Get the KSQL server status
        :return ksql-server version, clusterId'''
        response = self.get('/info')
        return response

    def get_topics(self):
        '''Get topics
        :return list of topic properties'''
        response = self.post('/ksql', data=LIST_TOPICS)
        return response.json()[0]['topics']

    def get_streams(self):
        '''Get streams
        :return list of streams'''
        response = self.post('/ksql', data=LIST_STREAMS)
        return response.json()[0]['streams']

    def get_tables(self):
        '''Get tables
        :return list of tables'''
        response = self.post('/ksql', data=LIST_TABLES)
        return response.json()[0]['tables']

    def get_queries(self):
        '''Get queries
        :return list of queries'''
        response = self.post('/ksql', data=LIST_QUERIES)
        return response.json()[0]['queries']

    def get_description(self, table_or_stream=None):
        '''Get DESCRIBE EXTENDED
        :return json of description of a table or stream'''
        if table_or_stream is not None:
            statement = {"ksql": f"DESCRIBE EXTENDED {table_or_stream};",
                         "streamsProperties": {"ksql.streams.auto.offset.reset": KSQL_OFFSET}}
            response = self.post('/ksql', data=statement)
            return response.json()[0]
        else:
            pass

    def run_query(self, query=None, auto_offset_reset=KSQL_OFFSET):
        '''Get data row by row
        :return list of row, the last element is about if terminal=true'''
        if query is not None:
            statement = {"ksql": query,
                         "streamsProperties": {"ksql.streams.auto.offset.reset": auto_offset_reset}}

            response = self.post('/query', data=statement)

            if query.split(' ')[0].upper() == 'SELECT':
                list_of_rows = response.content.decode(ENCODING).replace('\n\n', '').split('\n')
                list_of_rows.remove('')  # remove empty last element
                exec_status = list_of_rows[-1]  # get the status of the termination
                row_data_list = [json.loads(row)['row']['columns'] for row in list_of_rows[:-1]]  # get the row data
                df = pd.DataFrame(row_data_list)

                # TODO: get the name of column, need to parse the query or wait for the KSQL update.
                # TODO: add syntax analyser to figure out if stream or table or topic exists
                # TODO: add indicator of query
                return df, exec_status
        else:
            pass
