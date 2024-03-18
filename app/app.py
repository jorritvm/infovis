"""
This is the main file for the dash app
"""

import os
from dotenv import load_dotenv

from dash import Dash, page_container, html
import dash_bootstrap_components as dbc
from components.header import header
from components.sidebar import sidebar


app = Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME],
)
# app.layout = html.Div([navbar, page_container])
app.layout = dbc.Container(
    [
        dbc.Row(header),
        dbc.Row(
            [
                dbc.Col([sidebar], xs=3, sm=4, md=2, lg=2, xl=2, xxl=2),
                dbc.Col([page_container], xs=8, sm=8, md=10, lg=10, xl=10, xxl=10),
            ]
        ),
    ],
    fluid=True,
)

if __name__ == "__main__":
    load_dotenv()
    SERVER_PORT = os.getenv("SERVER_PORT")

    app.run_server(port=SERVER_PORT, debug=True)
