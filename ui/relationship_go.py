import json
import urllib

import dash
import dash_core_components as dcc
import plotly.graph_objects as go

go_components = [dcc.Dropdown(
    id='my-dropdown',
    options=[
        {'label': 'New York City', 'value': 'NYC'},
        {'label': 'Montreal', 'value': 'MTL'},
        {'label': 'San Francisco', 'value': 'SF'}
    ],
    value='NYC'
),
    dcc.Graph(
        id='graph',
        config={
            'showSendToCloud': True,
            'plotlyServerURL': 'https://plot.ly'
        },
    )]

go_callback_output = dash.dependencies.Output('graph', 'figure')
go_callback_input = [dash.dependencies.Input('my-dropdown', 'value')]


def go_callback_function(value):
    url = 'https://raw.githubusercontent.com/plotly/plotly.js/master/test/image/mocks/sankey_energy.json'
    response = urllib.request.urlopen(url)
    data = json.loads(response.read())
    fig = go.Figure(data=[go.Sankey(
        valueformat=".0f",
        valuesuffix="TWh",
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
            label=data['data'][0]['link']['label']
        ))])

    fig.update_layout(
        title_text="Energy forecast for 2050<br>Source: Department of Energy & Climate Change, Tom Counsell via <a href='https://bost.ocks.org/mike/sankey/'>Mike Bostock</a>",
        font_size=10)

    return fig
