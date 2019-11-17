import json
import urllib
from textwrap import dedent as d

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import randomcolor

rand_color = randomcolor.RandomColor()

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}
go_components = [dcc.RadioItems(
    id='my-radio-items',
    options=[
        {'label': 'Free to move', 'value': 'freeform'},
        {'label': 'Fixed', 'value': 'fixed'},
        {'label': 'Perpendicular', 'value': 'perpendicular'},
        {'label': 'Snap', 'value': 'snap'}
    ],
    value='snap'),
    dcc.Graph(
        id='basic-interactions',
        config={
            'showSendToCloud': True,
            'plotlyServerURL': 'https://plot.ly'
        },
    ),
    html.Div([
        dcc.Markdown(d("""
                **Hover Data**

                Mouse over values in the graph.
            """)),
        html.Pre(id='hover-data', style=styles['pre'])
    ], className='three columns'),

    html.Div([
        dcc.Markdown(d("""
                **Click Data**

                Click on points in the graph.
            """)),
        html.Pre(id='click-data', style=styles['pre']),
    ], className='three columns')
]

go_callback_output = dash.dependencies.Output('basic-interactions', 'figure')
go_callback_input = [dash.dependencies.Input('my-radio-items', 'value')]


def go_callback_function(value):
    url = 'https://raw.githubusercontent.com/plotly/plotly.js/master/test/image/mocks/sankey_energy.json'
    response = urllib.request.urlopen(url)
    data = json.loads(response.read())
    fig = go.Figure(data=[go.Sankey(
        valueformat=".0f",
        valuesuffix="TWh",
        arrangement=value or 'snap',
        # Define nodes
        node=dict(
            pad=15,
            thickness=15,
            line=dict(color="black", width=0.5),
            label=data['data'][0]['node']['label'],
            color=data['data'][0]['node']['color']
        ),
        # Add links
        link=dict(
            source=data['data'][0]['link']['source'],
            target=data['data'][0]['link']['target'],
            value=data['data'][0]['link']['value'],
            label=data['data'][0]['link']['label'],
            color=rand_color.generate(count=len(data['data'][0]['link']['label']))
        ))])

    fig.update_layout(
        title_text="Energy forecast for 2050<br>Source: Department of Energy & Climate Change, Tom Counsell via <a href='https://bost.ocks.org/mike/sankey/'>Mike Bostock</a>",
        font_size=10,
        clickmode='event+select',
        height=750,
        updatemenus=[
            dict(
                y=0.9,
                buttons=[
                    dict(
                        label='Thick',
                        method='restyle',
                        args=['node.thickness', 20]
                    ),
                    dict(
                        label='Thin',
                        method='restyle',
                        args=['node.thickness', 8]
                    )
                ]
            ),
            dict(
                y=0.8,
                buttons=[
                    dict(
                        label='Small gap',
                        method='restyle',
                        args=['node.pad', 15]
                    ),
                    dict(
                        label='Large gap',
                        method='restyle',
                        args=['node.pad', 20]
                    )
                ]
            ),
            dict(
                y=0.7,
                buttons=[
                    dict(
                        label='Snap',
                        method='restyle',
                        args=['arrangement', 'snap']
                    ),
                    dict(
                        label='Perpendicular',
                        method='restyle',
                        args=['arrangement', 'perpendicular']
                    ),
                    dict(
                        label='Freeform',
                        method='restyle',
                        args=['arrangement', 'freeform']
                    ),
                    dict(
                        label='Fixed',
                        method='restyle',
                        args=['arrangement', 'fixed']
                    )
                ]
            ),
            dict(
                y=0.6,
                buttons=[
                    dict(
                        label='Horizontal',
                        method='restyle',
                        args=['orientation', 'h']
                    ),
                    dict(
                        label='Vertical',
                        method='restyle',
                        args=['orientation', 'v']
                    )
                ])]
    )
    return fig


go_display_hover_data_callback_output = dash.dependencies.Output('hover-data', 'children')
go_display_hover_data_callback_input = [dash.dependencies.Input('basic-interactions', 'hoverData')]
go_display_click_data_callback_output = dash.dependencies.Output('click-data', 'children')
go_display_click_data_callback_input = [dash.dependencies.Input('basic-interactions', 'clickData')]


def go_display_hover_data_function(hoverData):
    return json.dumps(hoverData, indent=2)


def go_display_click_data_function(clickData):
    return json.dumps(clickData, indent=2)
