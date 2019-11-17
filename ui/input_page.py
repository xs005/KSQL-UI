import dash_core_components as dcc

input_textarea_layout = dcc.Textarea(
    placeholder='Enter a query here...',
    value='SELECT * FROM SOME_STREAM;',
    style={'width': '100%'}
)