"""
This is the main file for the dash app
"""
import os
from dotenv import load_dotenv

import pandas as pd
import dash
from dash import dcc, html, Input, Output
import dash_leaflet as dl
import dash_leaflet.express as dlx
import dash_bootstrap_components as dbc
import plotly.express as px

#############################
# data transformations
#############################
dfd = pd.read_parquet("../data/clean/gwpt.parquet")  # full details
agg = pd.read_parquet("../data/clean/gwpt_agg.parquet")  # aggregated only
geo = pd.read_parquet("../data/clean/geo.parquet")  # geo info only


def filter_df(dfi, region=None, sub_region=None, country=None, status=None, time_range=None):
    dfo = dfi.copy()

    # filter by region
    if region is not None:
        if region != "Total":
            dfo = dfo[(dfo["Region"] == region)]

    # filter by sub_region
    if sub_region is not None:
        dfo = dfo[(dfo["Subregion"] == sub_region)]

    # filter by country
    if country is not None:
        dfo = dfo[(dfo["Country"] == country)]

    # filter by status
    if status is not None and status != []:
        dfo = dfo[dfo["Status"].isin(status)]

    # filter by time range
    if time_range is not None:
        start_year, end_year = time_range
        dfo = dfo[(dfo["Start year"] >= start_year) & (dfo["Start year"] <= end_year)]

    return dfo


#############################
# APP definition
#############################
# create the app
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.SLATE, dbc.icons.FONT_AWESOME],
)

# create the cards
continents = ["Total"] + list(geo["Region"].unique())
continents_dbc = []
for continent in continents:
    # to make it clickable I wrap the dbc card in an html div
    continent_dbc = dbc.Button([
                html.H4(f"{continent} Capacity", className="card-title"),
                html.H6("", className="card-subtitle", id=f"{continent}_capacity")
            ],
            id=f"{continent}_click",
            outline=False,
            color="secondary",
            size="lg")
    continents_dbc = continents_dbc + [continent_dbc]

# create the filters
sub_region_filter = dcc.Dropdown(
    id='sub_region_filter',
    options=[]
)
country_filter = dcc.Dropdown(
    id='country_filter',
    options=[]
)
unique_status = list(dfd["Status"].unique())
unique_status.sort()
status_filter = dcc.Dropdown(
    id='status_filter',
    options=unique_status,
    multi=True,
)
y_min = min(dfd["Start year"].min(), dfd["Retired year"].min())
y_max = max(dfd["Start year"].max(), dfd["Retired year"].max())
time_slider = dcc.RangeSlider(
    id='time_slider',
    min=y_min,
    max=y_max,
    step=1,
    marks={i: str(i) for i in range(y_min, y_max+1) if i % 10 == 0},
    value=[y_min, y_max]  # Default value
)

# create the app's layout
app.layout = dbc.Container([
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
                    dbc.Row(
                        html.Div("main map content",
                                 id="main_map",
                                 style={}),
                        style={'height': '85vh'}),
                    style={'height': '85vh'},
                    width=9),
                dbc.Col(  # barchart column
                    dbc.Row(
                        html.Div("bar chart content",
                                 id="bar_chart",
                                 style={}),
                        style={'height': '85vh'}),
                    style={'height': '85vh'},
                    width=3),
                ],
                style={'height': '85vh'}),
            ], width=10)
        ]),
    ], fluid=True
)

##################
# callbacks
##################
@app.callback(
    [Output(f"{continent}_capacity", 'children') for continent in continents],
    [Input('status_filter', 'value'),
     Input('time_slider', 'value')]
)
def update_capacities_on_cards(status, time_range):
    # Filter DataFrame based on status and time range
    dff = filter_df(agg, status=status, time_range=time_range)

    # make output values for every continent
    output_capacities = []
    for continent in continents:
        if continent == "Total":
            capa = dff["Capacity (MW)"].sum()
        else:
            capa = dff[dff["Region"] == continent]["Capacity (MW)"].sum()
        output_capacities = output_capacities + [capa]

    # format output
    output_capacities = [round(x) for x in output_capacities]  # round
    output_capacities = [f"{x:,}" for x in output_capacities]  # put thousand sep ,
    output_capacities = [x.replace(",",".") for x in output_capacities]  # put thousand sep .
    output_capacities = [f"{x} MW" for x in output_capacities]  # adding the SI unit .
    return output_capacities


@app.callback(
    Output("sub_region_filter", 'options'),
    [Input(f"{continent}_click", 'n_clicks') for continent in continents]
)
def update_subregion_filter(*button_clicks):
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
    if sub_region == "" or sub_region is None:
        return []
    else:
        countries = agg[agg["Subregion"] == sub_region]["Country"].unique()
        return countries


@app.callback(
    Output('main_map', 'children'),
    [Input('sub_region_filter', 'value'),
     Input('country_filter', 'value'),
     Input('status_filter', 'value'),
     Input('time_slider', 'value')]
)
def update_map(sub_region, country, status, time_range):
    # Filter DataFrame based on status and time range
    dff = filter_df(dfd, sub_region=sub_region, country=country, status=status, time_range=time_range)

    # debug it is way too slow so we just limit ourselves to 100 circles
    dff = dff.nlargest(100, "Capacity (MW)")

    # Create a list of dl.Marker objects for each wind farm
    markers = []
    for i, row in dff.iterrows():
        marker = dict(lat= row['Latitude'],
                 lon= row['Longitude'],
                 value=row['Capacity (MW)'])
        markers = markers + [marker]
    geojson = dlx.dicts_to_geojson(markers)
    print(geojson)

    # Putting the map in our app layout
    my_map = dl.Map([dl.TileLayer(),
                dl.GeoJSON(data=geojson, id="geojson", zoomToBounds=True)],
               style={'width': '100%', 'height': '100%'})

    # debug, none of the above works, so just show a basemap for now:
    my_map = dl.Map(dl.TileLayer(), center=[56,10], zoom=6, style={'width': '100%', 'height': '100%'})

    return my_map

@app.callback(
    Output('bar_chart', 'children'),
    [Input('sub_region_filter', 'value'),
     Input('country_filter', 'value'),
     Input('status_filter', 'value'),
     Input('time_slider', 'value')]
)
def update_bar_chart(sub_region, country, status, time_range):
    # Filter DataFrame based on status and time range
    dff = filter_df(dfd, sub_region=sub_region, country=country, status=status, time_range=time_range)

    # Sort DataFrame by capacity in descending order and select top 20 wind farms
    top_20 = dff.nlargest(20, "Capacity (MW)")
    top_20 = top_20[::-1]

    # Create horizontal bar chart
    fig = px.bar(top_20, x='Capacity (MW)', y='Project Name', orientation='h')
    fig.update_layout(title_text="Top 20 Largest Wind Farms")

    # Convert the Plotly figure to a Dash component
    graph = dcc.Graph(figure=fig, style={'width': '100%', 'height': '100%'})

    return graph


if __name__ == "__main__":
    load_dotenv()
    SERVER_PORT = os.getenv("SERVER_PORT")

    # run the server - debug=True auto reloads browser when dev makes changes
    app.run_server(port=SERVER_PORT, debug=True)

