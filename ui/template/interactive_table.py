import dash_table
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

from backend.entities.Topic import Topic
from backend.rest import REST

rest = REST()
df = Topic(rest.get_topics()).df

interactive_table_layout = html.Div(
    dash_table.DataTable(
        id='customer-table',
        columns=[
            {'name': i, 'id': i, 'deletable': True} for i in df.columns
            if i not in ['id', 'CUSTOMER']
        ],
        style_header={
            'backgroundColor': 'orange',
            'fontWeight': 'bold'
        },
        editable=False,
        filter_action="native",
        sort_action="native",
        sort_mode='multi',
        row_selectable='multi',
        row_deletable=False,
        selected_rows=[],
        page_action='native',
        page_current=0,
        page_size=10,
        style_cell_conditional=[
            {
                'if': {'column_id': c},
                'textAlign': 'left'
            } for c in ['LOAD_DATE']
        ],
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(255, 231, 214)'
            },
            {
                'if': {
                    'column_id': 'MSSQL-KAKFA',
                    'filter_query': '{MSSQL-KAKFA} = 0'
                },
                'backgroundColor': '#3D9970',
                'color': 'white',
                'fontWeight': 'bold',
            },
            {
                'if': {
                    'column_id': 'MSSQL-PGSQL',
                    'filter_query': '{MSSQL-PGSQL} = 0'
                },
                'backgroundColor': '#3D9970',
                'color': 'white',
                'fontWeight': 'bold',
            }
        ],
    ),
)
