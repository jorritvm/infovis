"""
This is the main file for the dash app
"""

import os
from dotenv import load_dotenv

import pandas as pd
import dash
# from dash import dcc
from dash import html
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
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME],
)

# create the cards
card_total = dbc.Card(
    dbc.CardBody([html.H4("Total Capacity", className="card-title"),
                  html.H6("", className="card-subtitle")]),
    style={"width": "18rem"}
)
card_continent = dict()
for continent in geo["Region"].unique():
    card_continent[continent] = dbc.Card(
        dbc.CardBody([html.H5(f"{continent} Capacity", className="card-title"),
                      html.H6("", className="card-subtitle")]),
        style={"width": "18rem"}
    )
all_cards = [card_total] + list(card_continent.values())

# create the main map
main_map = html.Div("main map content", style={'background-color': 'green'})

# create the bar chart
bar_chart = html.Div("bar chart content", style={'background-color': 'red'})

# create the app's layout
app.layout = dbc.Container([
    dbc.Row([html.H1("Global wind power tracker analysis",
                     className='text-center mb-4',
                     style={'height': '25px'})]),
    dbc.Row([
        dbc.Col( # sidebar column
            [dbc.Row(x, style={'height': '15vh'}) for x in all_cards],
            style={'background-color': 'lightblue', 'height': '100vh'},
            width=2),
        dbc.Col([
            dbc.Row( # filters row
                "filters",
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


if __name__ == "__main__":
    load_dotenv()
    SERVER_PORT = os.getenv("SERVER_PORT")

    # run the server - debug=True auto reloads browser when dev makes changes
    app.run_server(port=SERVER_PORT, debug=True)
