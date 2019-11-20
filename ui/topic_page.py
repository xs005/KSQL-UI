import dash_table

from backend.entities.Topic import Topic
from backend.rest import REST

rest = REST()
df = Topic(rest.get_topics()).df
topic_table_layout = dash_table.DataTable(
    id='topic_table',
    columns=[{"name": i, "id": i} for i in df.columns],
    data=df.to_dict('records'),
)
