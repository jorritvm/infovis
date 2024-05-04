"""
this module contains utilities functions for the app
"""

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


def filter_data(df, clicked_continent, status, time_range):
    # Filter DataFrame based on status and time range
    filtered_df = df.copy()

    # Filter by clicked continent
    if clicked_continent != "Total":
        filtered_df = filtered_df[filtered_df["Region"] == clicked_continent]

    # Filter by status
    if status is not None and status != []:
        filtered_df = filtered_df[filtered_df["Status"].isin(status)]

    # Filter by time range
    if time_range is not None:
        start_year, end_year = time_range
        filtered_df = filtered_df[(filtered_df["Start year"] >= start_year) & (filtered_df["Start year"] <= end_year)]

    return filtered_df
