from unittest import TestCase

from backend.label import Label
from backend.relationship import Relationship
from backend.rest import REST


class TestREST(TestCase):

    def setUp(self):
        self.r = REST()

    def test_get_status(self):
        status = self.r.get_status()
        print(status)

    def test_get_queries(self):
        queries = self.r.get_queries()
        print(queries)

    def test_get_streams(self):
        streams = self.r.get_streams()
        print(streams)

    def test_get_tables(self):
        tables = self.r.get_tables()
        print(tables)

    def test_get_topics(self):
        topics = self.r.get_topics()
        print(topics)

    def test_run_query(self):
        select_query_df, resp = self.r.run_query(
            query='''SELECT * FROM NYC_TAXI2 LIMIT 10;''')
        print(select_query_df)
        print(resp)

        create_query = self.r.run_query(
            query='''CREATE STREAM NYC_TAXI3 WITH(KAFKA_TOPIC='nyc_yellow_taxi_trip_data', VALUE_FORMAT='AVRO');''')
        print(create_query)

    def test_get_descrption(self):
        stream_list = [i['name'] for i in self.r.get_streams()]
        table_list = [i['name'] for i in self.r.get_tables()]

        description_list = []
        for i in stream_list + table_list:
            t = self.r.get_description(table_or_stream=i)
            description_list.append(t)
            print('\n', i, '\n',
                  t['sourceDescription']['topic'], '\n',
                  t['sourceDescription']['readQueries'], '\n',
                  t['sourceDescription']['writeQueries'], '\n',
                  t)
        # print(description_list)

    def test_relationship(self):
        r = Relationship()
        query_dict = r.query_dict
        relaionship_list = r.relationship_list

        l = Label(relaionship_list)
        source_list = l.source_list
        target_list = l.target_list

        print(source_list, target_list)

        print(query_dict, '\n')

        print(relaionship_list)
