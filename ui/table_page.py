import dash_table

from backend.entities.Table import Table
from backend.rest import REST

rest = REST()
df = Table(rest.get_tables()).df
table_table_layout = dash_table.DataTable(
    id='table_table',
    columns=[{"name": i, "id": i} for i in df.columns],
    data=df.to_dict('records'),
)
