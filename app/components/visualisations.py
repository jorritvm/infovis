from dash import dcc
import plotly.graph_objects as go


def blank_figure():
    """
    create blank figure to show during initial loading
    Returns: a blank plotly graphics object
    """
    fig = go.Figure(go.Scatter(x=[], y=[]))
    fig.update_layout(template=None)
    fig.update_xaxes(showgrid=False, showticklabels=False, zeroline=False)
    fig.update_yaxes(showgrid=False, showticklabels=False, zeroline=False)
    return fig


# create the main map
main_map = dcc.Graph(id='main_map', figure=blank_figure())

# create the bar chart
bar_chart = dcc.Graph(id='bar_chart', figure=blank_figure())
