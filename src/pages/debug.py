import os

import dash
from dash import html


dash.register_page(__name__)


layout = html.Div(
    [
        html.H1("Debug page - put 'test' code here..."),
        html.P(f"e.g. what's the current wd? {os.getcwd()}"),
        html.Hr(),
    ],
    style={"margin": "20px"},
)
