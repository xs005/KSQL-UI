import dash
import dash_core_components as dcc
import dash_html_components as html

page_2_layout = html.Div([
    html.H1('Page 2'),
    dcc.RadioItems(
        id='page-2-radios',
        options=[{'label': i, 'value': i} for i in ['Orange', 'Blue', 'Red']],
        value='Orange'
    ),
    html.Div(id='page-2-content'),
    html.Br(),
    dcc.Link('Go to Page 1', href='/page-1'),
    html.Br(),
    dcc.Link('Go back to home', href='/')
])

page_2_callback_output = dash.dependencies.Output('page-2-content', 'children')
page_2_callback_input = [dash.dependencies.Input('page-2-radios', 'value')]
