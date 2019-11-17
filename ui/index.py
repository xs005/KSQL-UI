import dash
import dash_core_components as dcc
import dash_html_components as html

from ui.query_page import query_table_layout
from ui.relationship_go import go_callback_output, go_callback_input, go_components, go_callback_function, \
    go_display_click_data_callback_input, go_display_click_data_callback_output, go_display_hover_data_callback_output, \
    go_display_hover_data_callback_input, go_display_hover_data_function, go_display_click_data_function
from ui.stream_page import stream_table_layout
from ui.table_page import table_table_layout
from ui.topic_page import topic_table_layout

print(dcc.__version__)  # 0.6.0 or above is required

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Since we're adding callbacks to elements that don't exist in the app.layout,
# Dash will raise an exception to warn us that we might be
# doing something wrong.
# In this case, we're adding the elements through a callback, so we can ignore
# the exception.
app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

index_page = html.Div([dcc.Link('Topics', href='/topics'),
                       html.Br(),
                       dcc.Link('Streams', href='/streams'),
                       html.Br(),
                       dcc.Link('Tables', href='/tables'),
                       html.Br(),
                       dcc.Link('Queries', href='/queries'),
                       ] + go_components)

page_topics = topic_table_layout
page_streams = stream_table_layout
page_tables = table_table_layout
page_queries = query_table_layout


# Update the index
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/topics':
        return page_topics
    elif pathname == '/streams':
        return page_streams
    elif pathname == '/tables':
        return page_tables
    elif pathname == '/queries':
        return page_queries
    else:
        return index_page
    # You could also return a 404 "URL not found" page here


@app.callback(go_callback_output,
              go_callback_input)
def update_output(value):
    return go_callback_function(value)


@app.callback(go_display_hover_data_callback_output,
              go_display_hover_data_callback_input)
def display_hover_data(hoverData):
    return go_display_hover_data_function(hoverData)


@app.callback(go_display_click_data_callback_output,
              go_display_click_data_callback_input)
def display_click_data(clickData):
    return go_display_click_data_function(clickData)


if __name__ == '__main__':
    app.run_server(debug=True, port=8052)
