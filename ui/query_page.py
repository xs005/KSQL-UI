import dash_table

from backend.entities.Query import Query
from backend.rest import REST

rest = REST()
df = Query(rest.get_queries()).df
query_table_layout = dash_table.DataTable(
    id='query_table',
    columns=[{"name": i, "id": i} for i in df.columns],
    data=df.to_dict('records'),
)
