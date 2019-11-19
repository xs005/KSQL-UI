import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table

from backend.rest import REST

input_query_layout = [
    dcc.Textarea(id='input-query-statement',
                 placeholder='Enter a query here...',
                 value='SELECT * FROM SOME_TABLE_OR_STREAM LIMIT 10;',
                 style={'width': '100%'}),
    html.Div('set \'auto.offset.reset\'='),
    dcc.RadioItems(id='auto-offset-reset',
                   options=[
                       {'label': 'earliest', 'value': 'earliest'},
                       {'label': 'latest', 'value': 'latest'}
                   ],
                   value='earliest',
                   labelStyle={'display': 'inline-block'}),
    html.Button('SUBMIT', id='submit-query'),
    html.Div(id='query-feedback')
]

input_query_callback_output = dash.dependencies.Output('query-feedback', 'children')
input_query_callback_input = [dash.dependencies.Input('submit-query', 'n_clicks')]
input_query_callback_state = [dash.dependencies.State('input-query-statement', 'value'),
                              dash.dependencies.State('auto-offset-reset', 'value')]


def input_query_function(n_clicks, input_query_statement, auto_offset_reset):
    if n_clicks is not None:  # prevent startup running callback

        # send the query to KSQL server
        df, status = REST().run_query(input_query_statement, auto_offset_reset)

        if df.shape[0] == 0:
            table_layout = html.Div([
                html.Div(status),
                html.Div('No Data/Topic/Stream/Table/Query is found.'),
            ])
        else:
            table_layout = html.Div([
                dash_table.DataTable(
                    id='input-query-return-data',
                    columns=[{"name": str(i), "id": str(i)} for i in df.columns],
                    data=df.to_dict('records'),
                ),
                html.Div(status)])

        return table_layout
