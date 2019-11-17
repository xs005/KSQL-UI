import pandas as pd


class Stream:
    def __init__(self, dict_list):
        self.stream_list = dict_list

        self.df = self.transform()

    def transform(self):
        name_list = []
        topic_list = []
        format_list = []
        for stream_info in self.stream_list:
            name_list.append(stream_info['name'])
            topic_list.append(stream_info['topic'])
            format_list.append(stream_info['format'])

        df = pd.DataFrame({'name': name_list,
                           'topic': topic_list,
                           'format': format_list})

        return df
