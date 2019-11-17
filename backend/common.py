KSQL_SERVER_URL = 'http://127.0.0.1:8088'

KSQL_OFFSET = "earliest"
ENCODING = "utf-8"

HEADER = {"Content-Type": "application/vnd.ksql.v1+json; charset=utf-8", "Accept": "application/vnd.ksql.v1+json"}

LIST_STREAMS = {"ksql": "LIST STREAMS;", "streamsProperties": {"ksql.streams.auto.offset.reset": KSQL_OFFSET}}
LIST_TABLES = {"ksql": "LIST TABLES;", "streamsProperties": {"ksql.streams.auto.offset.reset": KSQL_OFFSET}}
LIST_QUERIES = {"ksql": "LIST QUERIES;", "streamsProperties": {"ksql.streams.auto.offset.reset": KSQL_OFFSET}}
LIST_TOPICS = {"ksql": "LIST TOPICS;", "streamsProperties": {"ksql.streams.auto.offset.reset": KSQL_OFFSET}}
