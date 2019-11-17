import pandas as pd


class Query:
    def __init__(self, dict_list):
        self.query_list = dict_list

        self.df = self.transform()

    def transform(self):
        id_list = []
        topic_list = []
        query_string_list = []
        for query_info in self.query_list:
            id_list.append(query_info['id'])
            topic_list.append(query_info['sinks'][0])
            query_string_list.append(query_info['queryString'])

        df = pd.DataFrame({'id': id_list,
                           'topic': topic_list,
                           'query': query_string_list})

        return df
