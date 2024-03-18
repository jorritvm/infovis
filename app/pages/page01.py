import dash
from dash import html

dash.register_page(__name__, path="/")

layout = html.Div(
    [html.H1("Page 01"), html.P("to be completed")], style={"margin": "20px"}
)
