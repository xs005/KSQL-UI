import json
from textwrap import dedent as d

import dash
import dash_core_components as dcc
import dash_html_components as html

from backend.common import STYLES
from backend.sankey_diagram import sankey_diagram

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

    html.Div([
        dcc.Markdown(d("""
                **Click Data**

                Click on points in the graph.
            """)),
        html.Pre(id='click-data', style=STYLES['pre']),
    ], className='three columns')
]

go_display_hover_data_callback_output = dash.dependencies.Output('hover-data', 'children')
go_display_hover_data_callback_input = [dash.dependencies.Input('basic-interactions', 'hoverData')]
go_display_click_data_callback_output = dash.dependencies.Output('click-data', 'children')
go_display_click_data_callback_input = [dash.dependencies.Input('basic-interactions', 'clickData')]


def go_display_hover_data_function(hoverData):
    return json.dumps(hoverData, indent=2)


def go_display_click_data_function(clickData):
    return json.dumps(clickData, indent=2)
