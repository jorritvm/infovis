import dash
from dash import html

dash.register_page(__name__)

layout = html.Div([
    html.H1("404"),
    html.P("Page content cannot be found.")
],
style={"margin": "20px"})