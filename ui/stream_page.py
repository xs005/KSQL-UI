import dash_table

from backend.entities.Stream import Stream
from backend.rest import REST

rest = REST()
df = Stream(rest.get_streams()).df
stream_table_layout = dash_table.DataTable(
    id='stream_table',
    columns=[{"name": i, "id": i} for i in df.columns],
    data=df.to_dict('records'),
)
