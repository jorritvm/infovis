import dash
from dash import html

dash.register_page(__name__)

layout = html.Div(
    [html.H1("Page 02"), html.P("to be completed")], style={"margin": "20px"}
)
