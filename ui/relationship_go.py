import json
from textwrap import dedent as d

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table

from backend.common import STYLES
from backend.entities.Stream import Stream
from backend.rest import REST
from backend.sankey_diagram import sankey_diagram, stream_list, table_list, link_labels

go_components = [
    dcc.Graph(
        id='basic-interactions',
        figure=sankey_diagram,
    ),
    html.Div([
        dcc.Markdown(d("""
                **Hover Data**

                Mouse over values in the graph.
            """)),
        html.Pre(id='hover-data', style=STYLES['pre'])
    ], className='three columns'),

    html.Div(id='click-data')
]

go_display_hover_data_callback_output = dash.dependencies.Output('hover-data', 'children')
go_display_hover_data_callback_input = [dash.dependencies.Input('basic-interactions', 'hoverData')]
go_display_click_data_callback_output = dash.dependencies.Output('click-data', 'children')
go_display_click_data_callback_input = [dash.dependencies.Input('basic-interactions', 'clickData')]


def go_display_hover_data_function(hoverData):
    return json.dumps(hoverData, indent=2)


def go_display_click_data_function(clickData):
    try:
        node_or_link = clickData['points'][0]['label']
        rest = REST()
        if node_or_link in stream_list:
            click_df = Stream(rest.get_streams()).df
            df = click_df.loc[click_df.name == node_or_link, :]
            return dash_table.DataTable(
                id='stream_table',
                columns=[{"name": i, "id": i} for i in df.columns],
                data=df.to_dict('records'))
        elif node_or_link in table_list:
            click_df = Stream(rest.get_tables()).df
            df = click_df.loc[click_df.name == node_or_link, :]
            return dash_table.DataTable(
                id='table_table',
                columns=[{"name": i, "id": i} for i in df.columns],
                data=df.to_dict('records'))
        elif node_or_link in link_labels:
            click_df = Stream(rest.get_queries()).df
            df = click_df.loc[click_df.id == node_or_link, :]
            return dash_table.DataTable(
                id='query_table',
                columns=[{"name": i, "id": i} for i in df.columns],
                data=df.to_dict('records'))
        else:  # this is topic
            click_df = Stream(rest.get_topics()).df
            df = click_df.loc[click_df.name == node_or_link, :]
            return dash_table.DataTable(
                id='stream_table',
                columns=[{"name": i, "id": i} for i in df.columns],
                data=df.to_dict('records'))
    except:
        return 'Please click the nodes or links.'
