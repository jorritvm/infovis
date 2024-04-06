"""
This is the main file for the dash app
"""

import os
from dotenv import load_dotenv

import pandas as pd
import dash
from dash import dcc, html, Input, Output
# import dash_leaflet as dl
# from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# load data
df = pd.read_parquet("../data/clean/gwpt.parquet")
agg = pd.read_parquet("../data/clean/gwpt_agg.parquet")
geo = pd.read_parquet("../data/clean/geo.parquet")

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
    id='sub_region_filter_dropdown',
    options=[]
)
country_filter = dcc.Dropdown(
    id='country_filter_dropdown',
    options=[]
)
unique_status = list(df["Status"].unique())
unique_status.sort()
status_filter = dcc.Dropdown(
    id='status_dropdown',
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
    marks={i: str(i) for i in range(y_min, y_max+1) if i%10 == 0},
    value=[y_min, y_max]  # Default value
)

# create the main map
main_map = html.Div("main map content", id="temp", style={'background-color': 'green'})

# create the bar chart
bar_chart = html.Div("bar chart content", style={'background-color': 'red'})

# create the app's layout
app.layout = dbc.Container([
    dbc.Row([html.H1("Global wind power tracker analysis",
                     className='text-center mb-4',
                     style={'height': '25px'})]),
    dbc.Row([
        dbc.Col( # sidebar column
            [dbc.Row(x, style={'height': '15vh'}) for x in continents_dbc],
            style={'background-color': 'lightblue', 'height': '100vh'},
            width=2),
        dbc.Col([
            dbc.Row([ # filters row
                dbc.Col(sub_region_filter, width=2),
                dbc.Col(country_filter, width=2),
                dbc.Col(status_filter, width=2),
                dbc.Col(time_slider, width=6)
                ],
                style={'background-color': 'lightblue', 'height': '5vh'}),
            dbc.Row([
                dbc.Col( # map column
                    dbc.Row(main_map, style={'height': '85vh'}),
                    style={'background-color': 'lightyellow', 'height': '85vh'},
                    width=9),
                dbc.Col( # barchart column
                    dbc.Row(bar_chart, style={'height': '85vh'}),
                    style={'background-color': 'pink', 'height': '85vh'},
                    width=3),
                ],
                style={'background-color': 'aqua', 'height': '85vh'}),
            ], width=10)
        ]),
    ], fluid=True
)


# callbacks
@app.callback(
    [Output(f"{continent}_capacity", 'children') for continent in continents],
    Input('status_dropdown', 'value')
)
def update_capacities_on_cards(status):
    # filter by status
    tmp = agg.copy()
    if status is not None and status != []:
        tmp = agg[agg["Status"].isin(status)]

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
    output_capacities = [x.replace(",",".") for x in output_capacities]  # put thousand sep .
    return output_capacities

@app.callback(
    Output("sub_region_filter_dropdown", 'options'),
    [Input(f"{continent}_click", 'n_clicks') for continent in continents]
)
def update_subregion_filter(*button_clicks):
    ctx = dash.callback_context
    if not ctx.triggered:
        button_id = None
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        continent = button_id.replace("_click", "")
        options = []
        if continent != "Total":
            options = agg[agg["Region"] == continent]["Subregion"].unique()

    return options



if __name__ == "__main__":
    load_dotenv()
    SERVER_PORT = os.getenv("SERVER_PORT")

    # run the server - debug=True auto reloads browser when dev makes changes
    app.run_server(port=SERVER_PORT, debug=True)

