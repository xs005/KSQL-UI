import pandas as pd


class Topic:
    def __init__(self, dict_list):
        self.topic_list = dict_list

        self.df = self.transform()

    def transform(self):
        name_list = []
        registered_list = []
        replica_list = []
        partition_list = []
        for topic_info in self.topic_list:
            name_list.append(topic_info['name'])
            registered_list.append(topic_info['registered'])
            # TODO: if the list has more than 1 unique value, meaning some partitions has different replicas, some broker is not available
            replica_list.append(', '.join(map(str, topic_info['replicaInfo'])))
            partition_list.append(len(topic_info['replicaInfo']))

        df = pd.DataFrame({'name': name_list,
                           'registered': registered_list,
                           'replica': replica_list,
                           'partition': partition_list})

        return df
