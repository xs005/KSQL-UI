import json
import logging

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

    def get_data(self, query=None):
        '''Get data row by row
        :return list of row, the last element is about if terminal=true'''
        if query is not None:
            statement = {"ksql": query,
                         "streamsProperties": {"ksql.streams.auto.offset.reset": KSQL_OFFSET}}

            response = self.post('/query', data=statement)
            list_of_rows = response.content.decode(ENCODING).replace('\n\n', '').split('\n')
            list_of_rows.remove('')
            return list_of_rows
        else:
            pass
