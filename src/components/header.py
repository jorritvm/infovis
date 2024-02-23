"""
Header
"""

import dash_bootstrap_components as dbc
from .theme_toggle import theme_toggle

# Navbar component
header = dbc.NavbarSimple(
    children=[
        theme_toggle,
    ],
    brand="Infovis header bar",
    brand_style={"marginLeft": "10px"},
    color="green",
    dark=True,
)
