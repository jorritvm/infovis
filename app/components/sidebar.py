"""
Navigation bar (app header)
"""

from dash import html
import dash_bootstrap_components as dbc

# Navbar component
sidebar = dbc.Nav(
    children=[
        dbc.NavItem(
            dbc.NavLink(
                [
                    html.I(className="fa fa-fw fa-light fa-bars-progress"),
                    "Page 01",
                ],
                href="/",
                active="exact",
            )
        ),
        dbc.NavItem(
            dbc.NavLink(
                [
                    html.I(className="fa fa-fw fa-light fa-bars-progress"),
                    "Page 02",
                ],
                href="/page02",
                active="exact",
            )
        ),
        html.Hr(),
        dbc.NavItem(
            dbc.NavLink(
                [html.I(className="fa fa-fw fa-solid fa-info"), "For developers"],
                href="/developers",
                active="exact",
            )
        ),
        html.Hr(),
        dbc.NavItem(dbc.NavLink("debug", href="/debug", active="exact")),
    ],
    vertical=True,
    pills=True,
    style={"margin-top": "20px"},
)
