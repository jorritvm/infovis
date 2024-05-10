"""
This is the main file for the dash app
"""

import os
from dotenv import load_dotenv

import pandas as pd
import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc

from callbacks import cb_bar_chart, cb_continent, cb_country_filter, cb_map, cb_sub_region
from components import filters
from components.visualisations import main_map, bar_chart


####################
# data
####################
df = pd.read_parquet("../data/clean/gwpt.parquet")
agg = pd.read_parquet("../data/clean/gwpt_agg.parquet")
geo = pd.read_parquet("../data/clean/geo.parquet")


####################
# app & components
####################
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.SLATE, dbc.icons.FONT_AWESOME, 'assets/css/styles.css'],
)

continents = filters.generate_continents(geo)
continents_dbc = filters.generate_continent_cards(continents)
sub_region_filter = filters.generate_sub_region_filter()
country_filter = filters.generate_country_filter()
status_filter = filters.generate_status_filter(df)
type_filter = filters.generate_type_filter(df)
time_slider = filters.generate_time_slider(df)


####################
# layout
####################
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
                dbc.Col(type_filter, width=2),
                dbc.Col(time_slider, width=4)
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
cb_continent.register_update_capacities(app, continents, df)
cb_continent.register_update_ban_style(app, continents)
cb_continent.register_update_clicked_continent(app, continents)
cb_sub_region.register_update_subregion_filter(app, continents, agg)
cb_sub_region.register_reset_subregion(app, continents)
cb_country_filter.register_update_country_filter(app, agg, continents)
cb_country_filter.register_reset_country(app, continents)
cb_map.register_update_map(app, df)
cb_bar_chart.register_update_bar_chart(app, df)


if __name__ == "__main__":
    load_dotenv()
    SERVER_PORT = os.getenv("SERVER_PORT")

    # run the server - debug=True auto reloads browser when the dev makes changes
    app.run_server(port=SERVER_PORT, debug=True)
