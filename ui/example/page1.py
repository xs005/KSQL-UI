import dash
import dash_core_components as dcc
import dash_html_components as html

page_1_layout = html.Div([
    html.H1('Page 1'),
    dcc.Dropdown(
        id='page-1-dropdown',
        options=[{'label': i, 'value': i} for i in ['LA', 'NYC', 'MTL']],
        value='LA'
    ),
    html.Div(id='page-1-content'),
    html.Br(),
    dcc.Link('Go to Page 2', href='/page-2'),
    html.Br(),
    dcc.Link('Go back to home', href='/'),
])

page_1_callback_output = dash.dependencies.Output('page-1-content', 'children')
page_1_callback_input = [dash.dependencies.Input('page-1-dropdown', 'value')]
