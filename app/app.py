"""
This is the main file for the dash app
"""

import os
from dotenv import load_dotenv

import pandas as pd
import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px

from utils.utils import *


# load data
df = pd.read_parquet("../data/clean/gwpt.parquet")
agg = pd.read_parquet("../data/clean/gwpt_agg.parquet")
geo = pd.read_parquet("../data/clean/geo.parquet")


####################
# app & components
####################
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.SLATE, dbc.icons.FONT_AWESOME, 'styles.css'],
)


# create the sidebar buttons (BAN's)
continents = ["Total"] + list(geo["Region"].unique())
continents_dbc = []
for continent in continents:
    continent_dbc = dbc.Button([
        html.H4(f"{continent} Capacity", className="card-title"),
        html.H6("", className="card-subtitle", id=f"{continent}_capacity")
    ],
        id=f"{continent}_click",
        outline=False,
        color="secondary",
        size="lg")
    continents_dbc = continents_dbc + [continent_dbc]

# create the filters & slider
sub_region_filter = dcc.Dropdown(
    id='sub_region_filter',
    options=[]
)

country_filter = dcc.Dropdown(
    id='country_filter',
    options=[]
)

unique_status = list(df["Status"].unique())
unique_status.sort()
status_filter = dcc.Dropdown(
    id='status_filter',
    options=unique_status,
    multi=True,
)
y_min = min(df["Start year"].min(), df["Retired year"].min())
y_max = max(df["Start year"].max(), df["Retired year"].max())
time_slider = dcc.RangeSlider(
    id='time_slider',
    min=y_min,
    max=y_max,
    step=1,
    marks={i: str(i) for i in range(y_min, y_max + 1) if i % 10 == 0},
    value=[y_min, y_max],  # Default value
    className='custom_white_text'  # Set the text color to white
)

# create the main map
main_map = dcc.Graph(id='main_map', figure=blank_figure())

# create the bar chart
bar_chart = dcc.Graph(id='bar_chart', figure=blank_figure())

# create the app's layout
app.layout = dbc.Container([
    dcc.Store(id='last_clicked_continent', data='Total'),  # Add this line here
    dbc.Row([html.H1("Global wind power tracker analysis",
                     className='text-center mb-4',
                     style={'height': '45px'})]),
    dbc.Row([
        dbc.Col(  # sidebar column
            [dbc.Row(x, style={'height': '15vh'}) for x in continents_dbc],
            style={'height': '100vh'},
            width=2),
        dbc.Col([
            dbc.Row([  # filters row
                dbc.Col(sub_region_filter, width=2),
                dbc.Col(country_filter, width=2),
                dbc.Col(status_filter, width=2),
                dbc.Col(time_slider, width=6)
            ],
                style={'height': '5vh'}),
            dbc.Row([
                dbc.Col(  # map column
                    dbc.Row(main_map, style={'height': '95vh'}),
                    width=9),
                dbc.Col(  # barchart column
                    dbc.Row(bar_chart, style={'height': '85vh'}),
                    style={'height': '85vh'},
                    width=3),
            ],
                style={'height': '85vh'}),
        ], width=10)
    ]),
], fluid=True
)


####################
# callbacks
####################
@app.callback(
    [Output(f"{continent}_capacity", 'children') for continent in continents],
    [Input('status_filter', 'value'),
     Input('time_slider', 'value')]
)
def update_capacities_on_cards(status, time_range):
    """
    Updates the values on the BAN's when the status dropdown or time_range has been modified
    Args:
        status: string
        time_range: tuple of (start_year, end_year)
    Returns:
        A list of strings, representing the capacities per continent
    """
    # filter by status
    tmp = df.copy()
    if status is not None and status != []:
        tmp = tmp[tmp["Status"].isin(status)]

    # filter by time range
    if time_range is not None:
        start_year, end_year = time_range
        tmp = tmp[(tmp["Start year"] >= start_year) & (tmp["Start year"] <= end_year)]

    # make output values for every continent
    output_capacities = []
    for continent in continents:
        if continent == "Total":
            capa = tmp["Capacity (MW)"].sum()
        else:
            capa = tmp[tmp["Region"] == continent]["Capacity (MW)"].sum()
        output_capacities = output_capacities + [capa]

    # format output
    output_capacities = [round(x) for x in output_capacities]  # round
    output_capacities = [f"{x:,}" for x in output_capacities]  # put thousand sep ,
    output_capacities = [x.replace(",", ".") for x in output_capacities]  # put thousand sep .
    output_capacities = [f"{x} MW" for x in output_capacities]  # adding the SI unit .
    return output_capacities


@app.callback(
    Output("sub_region_filter", 'options'),
    [Input(f"{continent}_click", 'n_clicks') for continent in continents]
)
def update_subregion_filter(*button_clicks):
    """
    Updates the available options in the subregion dropdown when the region BAN has been clicked
    Args:
        *button_clicks: not used
    Returns:
        a list of (string) sub region values
    """
    options = []
    ctx = dash.callback_context
    if ctx.triggered:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        continent = button_id.replace("_click", "")
        options = []
        if continent != "Total":
            options = agg[agg["Region"] == continent]["Subregion"].unique()
    return options


@app.callback(
    Output("country_filter", "options"),
    Input("sub_region_filter", "value")
)
def update_country_filter(sub_region):
    """
    Updates the available options in the country dropdown when the subregion filter has been selected
    Args:
        sub_region: string specifying a subregion
    Returns:
        list of (string) countries in this subregion
    """
    if sub_region == "" or sub_region is None:
        return []
    else:
        countries = agg[agg["Subregion"] == sub_region]["Country"].unique()
        return countries


@app.callback(
    Output('last_clicked_continent', 'data'),
    [Input(f"{continent}_click", 'n_clicks') for continent in continents]
)
def update_clicked_continent(*continent_clicks):
    """
    Update the data (dcc.store value) for the last clicked continent.

    Parameters:
    *continent_clicks: Variable number of input arguments representing the number of clicks for each continent.

    Returns:
    The name of the last clicked continent if a button was clicked, otherwise returns "Total".
    """
    ctx = dash.callback_context
    if ctx.triggered:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        clicked_continent = button_id.replace("_click", "")
        return clicked_continent
    else:
        return "Total"


# Define a callback to update the button style based on the last clicked continent
@app.callback(
    [Output(f"{continent}_click", 'color') for continent in continents],
    [Input('last_clicked_continent', 'data')]
)
def update_ban_style(last_clicked_continent):
    """
    Darkens the BAN that you have clicked on to show it has been selected

    Parameters:
    last_clicked_continent: string representing the currently active continent filter

    Returns:
    a list of color values for all the continent buttons 'color' prop
    """
    result = []
    for continent in continents:
        if continent == last_clicked_continent:
            result.append("info")
        else:
            result.append("secondary")
    return result


@app.callback(
    Output('main_map', 'figure'),
    [Input('last_clicked_continent', 'data'),
     Input('sub_region_filter', 'value'),
     Input('country_filter', 'value'),
     Input('status_filter', 'value'),
     Input('time_slider', 'value'),
     Input('main_map', 'relayoutData'),
     Input('bar_chart', 'clickData')]
)
def update_map(continent, sub_region, country, status, time_range, zoom_info, clickdata):
    """
    Update the map based on the selected status, time range, and clicked continent.

    Parameters:
    status (list): List of selected statuses.
    time_range (tuple): Start and end year of the selected time range.
    clicked_continent (str): Continent that was last clicked.

    Returns:
    dl.Map: Updated map with markers representing wind farms.
    """
    filtered_df = filter_data(df, continent, sub_region, country, status, time_range)

    agg_country = filtered_df.groupby(["Region", "Subregion", "Country", "Status", "Installation Type"]).agg(
        {"Capacity (MW)": "sum", "Latitude": "mean", "Longitude": "mean",
         "Start year": "mean"}).reset_index()

    if zoom_info and 'mapbox.zoom' in zoom_info:
        zoom_level = zoom_info['mapbox.zoom']
    else:
        zoom_level = 1

    if zoom_level >= 3:
        data = filtered_df  # Filter data based on zoom level
        marker_min = 3
        hover_name = 'Project Name'
        opacity = 0.7
    else:
        data = agg_country
        marker_min = 4
        hover_name = "Country"
        opacity = 1

    # Create a color mapping for the statuses (test based on https://colorbrewer2.org/#type=diverging&scheme=BrBG&n=6)
    color_mapping = {
        'construction': '#5ab4ac',
        'operating': '#01665e',
        'announced': '#d8b365',
        'mothballed': 'lightgrey',
        'cancelled': 'black',
        'pre-construction': '#c7eae5',
        'retired': '#666666',
        'shelved': '#d95f02'
    }

    fig = px.scatter_mapbox(data,
                            lat="Latitude",
                            lon="Longitude",
                            size="Capacity (MW)",
                            hover_name=hover_name,
                            hover_data={"Capacity (MW)": True,
                                        "Installation Type": True,
                                        "Latitude": False,
                                        "Longitude": False},
                            category_orders={'Status': ['operating', 'construction', 'pre-construction', 'announced',
                                                        'retired', 'mothballed', 'shelved', 'cancelled']
                                             },
                            color="Status",
                            color_discrete_map=color_mapping,
                            zoom=zoom_level,
                            opacity=opacity
                            )

    if zoom_info and 'mapbox.center' in zoom_info:
        fig.update_layout(
            mapbox=dict(
                center=dict(lat=zoom_info['mapbox.center']['lat'], lon=zoom_info['mapbox.center']['lon']),
                zoom=zoom_level
            ))

    # style=: Allowed values which do not require a Mapbox API token are 'open-street-map', 'white-bg', 'carto-positron',
    # 'carto-darkmatter', 'stamen-terrain', 'stamen-toner', 'stamen-watercolor' -> none of them works with cluster
    # therefore choose between: Allowed values which do require a Mapbox API token are 'basic', 'streets', 'outdoors',
    # 'light', 'dark', 'satellite', 'satellite- streets' -> 'light' or 'dark' shows colours of markers best
    fig.update_layout(mapbox_style="carto-positron")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    fig.update_traces(marker_sizemin=marker_min)

    fig.update_layout(legend=dict(
        yanchor="top",
        y=0.955,
        xanchor="right",
        x=1.2
    ))

    # Center and zoom to clicked project on bar chart
    # TODO: let this only run right after clicking on the bar chart
    if clickdata is not None:
        clicked_project = filtered_df[filtered_df['Project Name'] == clickdata['points'][0]['label']]
        fig.update_layout(mapbox_center_lat=float(clicked_project['Latitude']),
                          mapbox_center_lon=float(clicked_project['Longitude']),
                          mapbox_zoom=7)

    return fig


@app.callback(
    Output('bar_chart', 'figure'),
    [Input('last_clicked_continent', 'data'),
     Input('sub_region_filter', 'value'),
     Input('country_filter', 'value'),
     Input('status_filter', 'value'),
     Input('time_slider', 'value'),
     ]
)
def update_bar_chart(continent, sub_region, country, status, time_range):
    """
    Updates the plotly bar chart when the user modifies the status filter, time slider or clicks on another continent
    Args:
        status: list of selected status strings
        time_range: tuple of 2 integers (start & end year)
        continent: string value for last clicked continent
    Returns:
        plotly figure to update the bar chart
    """
    # filter the whole dataset
    dfx = filter_data(df, continent, sub_region, country, status, time_range)

    # aggregate onto project level: combine project phases and statusses
    dfx_agg = dfx.groupby(["Region", "Subregion", "Country", "Installation Type", "Project Name"]).agg(
        {"Capacity (MW)": "sum", "Latitude": "mean", "Longitude": "mean",
         "Start year": "mean"}).reset_index()

    # Sort DataFrame by capacity in descending order and select top 20 wind farms
    top_20 = dfx_agg.nlargest(20, "Capacity (MW)")
    top_20 = top_20[::-1]

    # Create horizontal bar chart
    fig = px.bar(top_20, x='Capacity (MW)', y='Project Name', orientation='h')
    fig.update_layout(title_text="Top 20 Largest Wind Farms")

    return fig


if __name__ == "__main__":
    load_dotenv()
    SERVER_PORT = os.getenv("SERVER_PORT")

    # run the server - debug=True auto reloads browser when the dev makes changes
    app.run_server(port=SERVER_PORT, debug=True)
