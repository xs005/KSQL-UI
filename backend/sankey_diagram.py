import plotly.graph_objects as go

from backend.label import Label
from backend.relationship import Relationship

# Find relationships
r = Relationship()
relaionship_list = r.relationship_list
stream_list = r.stream_list
table_list = r.table_list
link_labels = r.link_label_list

# Label each items
l = Label(relaionship_list, stream_list, table_list)
source_list = l.source_list
target_list = l.target_list
labels = l.label
node_colors = l.label_color
link_colors = l.label_link_color(link_labels)
link_values = l.label_link_value()

# Generate the diagram
sankey_diagram = go.Figure(data=[go.Sankey(
    valueformat=".0f",
    valuesuffix=" messages/s",

    # Define nodes
    node=dict(
        pad=15,
        thickness=15,
        line=dict(color="black", width=0.5),
        label=labels,
        color=node_colors
    ),

    # Add links
    link=dict(
        source=source_list,
        target=target_list,
        value=[1 for _ in link_values],
        label=link_labels,
        # color=link_colors
    ))])

sankey_diagram.update_layout(
    title_text="KSQL Server SanKey Diagram",
    font_size=10,
    clickmode='event+select',
    height=850,
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
                    label='Fixed',
                    method='restyle',
                    args=['arrangement', 'fixed']
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
