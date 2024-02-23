"""
Theme selector
"""

from dash_bootstrap_templates import ThemeSwitchAIO
import dash_bootstrap_components as dbc
from dash import html

url_theme1 = dbc.themes.FLATLY
url_theme2 = dbc.themes.DARKLY
theme_toggle = html.Div(ThemeSwitchAIO(
    aio_id="theme",
    themes=[url_theme2, url_theme1],
    icons={"left": "fa fa-sun", "right": "fa fa-moon"}),
    style={"margin-left": "100px"})
