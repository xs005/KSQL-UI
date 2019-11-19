from backend.rest import REST


class Relationship:
    def __init__(self):
        self.rest = REST()
        stream_list = [i['name'] for i in self.rest.get_streams()]
        table_list = [i['name'] for i in self.rest.get_tables()]
        self.tables_and_streams_list = table_list + stream_list
        self.query_dict = {}
        self.relationship_list = []

        # get relationships and queries
        self.run()

    def get_properties(self, table_or_stream):
        description = self.rest.get_description(table_or_stream=table_or_stream)
        read_queries = description['sourceDescription']['readQueries']
        write_queries = description['sourceDescription']['writeQueries']
        topic = description['sourceDescription']['topic']

        self.get_query(write_queries)
        self.get_query(read_queries)

        if write_queries and not read_queries:
            relationship = [[table_or_stream, topic]]
        elif read_queries and not write_queries:
            relationship = [[topic, table_or_stream]]
            relationship += [[table_or_stream, read_queries[i]['sinks'][0]] for i in range(len(read_queries))]
        elif write_queries and read_queries:
            relationship = [[table_or_stream, topic]]
            for i in range(len(write_queries)):
                for j in range(len(read_queries)):
                    relationship += [[write_queries[i]['sinks'][0], read_queries[j]['sinks'][0]]]

        # TODO: add query id as link label, add color for topic/steam/table
        self.relationship_list += relationship


    def get_query(self, query_list):
        if query_list:
            for query in query_list:
                query_id = query['id']
                if query_id not in self.query_dict:
                    self.query_dict[query_id] = query['queryString']

    def run(self):
        for i in self.tables_and_streams_list:
            self.get_properties(i)
