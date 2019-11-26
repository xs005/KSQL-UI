import dash
import dash_core_components as dcc
import dash_html_components as html

from ui.example.page1 import page_1_layout, page_1_callback_output, page_1_callback_input
from ui.example.page2 import page_2_layout, page_2_callback_output, page_2_callback_input
from ui.example.utils import callback_indicator

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

index_page = html.Div([
    dcc.Link('Go to Page 1', href='/page-1'),
    html.Br(),
    dcc.Link('Go to Page 2', href='/page-2'),
])

page_1 = page_1_layout
page_2 = page_2_layout


@app.callback(page_1_callback_output,
              page_1_callback_input)
def page_1_dropdown(value):
    return callback_indicator(value)


@app.callback(page_2_callback_output,
              page_2_callback_input)
def page_2_radios(value):
    return callback_indicator(value)


# Update the index
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page-1':
        return page_1
    elif pathname == '/page-2':
        return page_2
    else:
        return index_page
    # You could also return a 404 "URL not found" page here


if __name__ == '__main__':
    app.run_server(debug=True)
