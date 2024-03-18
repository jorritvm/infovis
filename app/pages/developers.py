import os

import dash
from dash import dcc, html

dash.register_page(__name__)

with open("../README.md") as readme_file:
    readme_contents = readme_file.read()

layout = html.Div([dcc.Markdown(readme_contents)], style={"margin": "20px"})
