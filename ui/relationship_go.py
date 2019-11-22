import json
from textwrap import dedent as d

import dash
import dash_core_components as dcc
import dash_html_components as html

from backend.common import STYLES
from backend.sankey_diagram import sankey_diagram, stream_list, table_list, link_labels
from backend.utils import generate_datatable
from ui import stream_page, table_page, query_page, topic_page

go_components = [
    dcc.Graph(
        id='basic-interactions',
        figure=sankey_diagram,
    ),
    html.Div([html.Div(id='click-data'),
              dcc.Markdown(d("""
                **Hover Data**

                Mouse over values in the graph.
            """)),
              html.Pre(id='hover-data', style=STYLES['pre'])
              ], className='three columns'),
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
        if node_or_link in stream_list:
            click_df = stream_page.df
            df = click_df.loc[click_df.name == node_or_link, :]
            return generate_datatable(df, 'click_table')
        elif node_or_link in table_list:
            click_df = table_page.df
            df = click_df.loc[click_df.name == node_or_link, :]
            return generate_datatable(df, 'click_table')
        elif node_or_link in link_labels and node_or_link.split(' ')[0].upper() not in ['SOURCE', 'SINK']:
            click_df = query_page.df
            df = click_df.loc[click_df.id == node_or_link, :]
            return generate_datatable(df, 'click_table')
        elif node_or_link.split(' ')[0].upper() in ['SOURCE', 'SINK']:
            return node_or_link
        else:  # this is topic
            click_df = topic_page.df
            df = click_df.loc[click_df.name == node_or_link, :]
            return generate_datatable(df, 'click_table')
    except:
        return 'Please click the nodes or links.'
