from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc


def generate_continents(geo):
    """Create a list of contintents"""
    continents = ["Total"] + list(geo["Region"].unique())
    return continents


def generate_continent_cards(continents):
    """Create a list of continent BAN's"""
    continents_dbc = []
    for continent in continents:
        continent_dbc = dbc.Button([
            html.H4(f"{continent} Capacity", className="card-title"),
            html.H6("", className="card-subtitle", id=f"{continent}_capacity")
        ],
            id=f"{continent}_click",
            outline=False,
            color="secondary",
            size="lg",
            className="no-rounded")
        continents_dbc = continents_dbc + [continent_dbc]
    return continents_dbc


def generate_sub_region_filter():
    """create the sub region filter"""
    sub_region_filter = dcc.Dropdown(
        id='sub_region_filter',
        placeholder="sub region",
        options=[]
    )
    return sub_region_filter


def generate_country_filter():
    """create the country filter"""
    country_filter = dcc.Dropdown(
        id='country_filter',
        placeholder="country",
        options=[]
    )
    return country_filter


def generate_status_filter(df):
    """create the status filter"""
    unique_status = list(df["Status"].unique())
    unique_status.sort()
    status_filter = dcc.Dropdown(
        id='status_filter',
        options=unique_status,
        multi=False,
        placeholder="status",
    )
    return status_filter


def generate_type_filter(df):
    """create the type filter"""
    unique_type = list(df["Installation Type"].unique())
    unique_type.sort()
    type_filter = dcc.Dropdown(
        id='type_filter',
        options=unique_type,
        multi=False,
        placeholder="type",
    )
    return type_filter


def generate_time_slider(df):
    """generate the time slider filter"""
    y_min = min(df["Start year"].min(), df["Retired year"].min())
    y_max = max(df["Start year"].max(), df["Retired year"].max())
    time_slider = dcc.RangeSlider(
        id='time_slider',
        min=y_min,
        max=y_max,
        step=1,
        marks={i: str(i) for i in range(y_min, y_max + 1) if i % 10 == 0},
        value=[y_min, y_max],  # Default value,
        tooltip={"placement": "bottom", "always_visible": True},
        className='custom_white_text'  # Set the text color to white
    )
    return time_slider
