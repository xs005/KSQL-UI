import json
import logging

import pandas as pd
import requests

from backend.utils import without_keys
from .common import (
    HEADER, KSQL_SERVER_URL, LIST_TOPICS, LIST_STREAMS, LIST_TABLES, LIST_QUERIES, KSQL_OFFSET, ACTION_LIST)

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
        statement = {"ksql": query,
                     "streamsProperties": {"ksql.streams.auto.offset.reset": auto_offset_reset}}

        action = query.split(' ')[0].upper()
        if action == 'SELECT':
            response = self.post('/query', data=statement)
            list_of_rows = response.text.replace('\n\n', '').split('\n')
            try:
                list_of_rows.remove('')  # remove empty last element
            except:
                pass
            row_data_list = [json.loads(row)['row']['columns'] for row in list_of_rows[:-1]]  # get the row data
            df = pd.DataFrame(row_data_list)

            # TODO: get the name of column, need to parse the query or wait for the KSQL update.
            # TODO: add syntax analyser to figure out if stream or table or topic exists
            # TODO: add indicator of query
            # return df, exec_status
            return df, self.check_response(action, response)
        elif action == 'PRINT':
            response = self.post('/query', data=statement)
            list_of_rows = response.text.replace('\n\n', '').split('\n')
            format_info = list_of_rows[0]
            data_info = list_of_rows[1:-1]
            row_time = [i.split(',')[0] for i in data_info]
            data_json_list = [i.split(',', 2)[-1].strip() for i in data_info[0:]]
            df = pd.read_json(','.join(data_json_list), orient='records', lines=True)
            df.insert(0, 'FORMAT', format_info.split(':')[-1])
            df.insert(0, 'ROW_TIME', row_time)
            return df, self.check_response(action, response)
        elif action in ACTION_LIST:
            response = self.post('/ksql', data=statement)
            return self.check_response(action, response)
        else:
            return pd.DataFrame(), f'Only support {", ".join(str(x) for x in ACTION_LIST)} and SELECT.'

    def check_response(self, action, response):
        reason = response.reason
        msg = response.text
        if reason == 'OK':
            if action in ACTION_LIST and action not in ['LIST', 'DESCRIBE']:
                msg = json.loads(msg)[0]['commandStatus']['message']
                return pd.DataFrame(), f'{reason}: {msg}'
            elif action == 'LIST':
                msg = list(json.loads(msg)[0].values())[2]
                return pd.DataFrame(msg), f'{reason}: {msg}'
            elif action == 'DESCRIBE':
                fields = json.loads(msg)[0]['sourceDescription']['fields']
                # reformat the two level dictionary in the list to one level
                reformat_dict_list = []
                for field in fields:
                    one_level_dict = {}
                    for k, v in field.items():
                        if isinstance(v, str):
                            one_level_dict[k] = v
                        elif isinstance(v, dict):
                            for k2, v2 in v.items():
                                one_level_dict[k + '_' + k2] = v2
                    reformat_dict_list.append(one_level_dict)
                msg = without_keys(json.loads(msg)[0]['sourceDescription'], 'fields')
                return pd.DataFrame(reformat_dict_list), f'{reason}: {msg}'
        else:
            if action in ACTION_LIST:
                return pd.DataFrame(), f'{reason}: {msg}'
            msg = json.loads(response.text)['message']
        return f'{reason}: {msg}'
