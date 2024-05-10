from dash import html, dcc, Dash
import plotly.express as px
import pandas as pd
import numpy as np

#px.set_mapbox_access_token(ADD TOKEN)

df = pd.read_parquet("../data/clean/gwpt.parquet")
df["Installation Type"] = df["Installation Type"].apply(lambda x: 'offshore' if str(x).lower().startswith('offshore') else x)
agg_country = df.groupby(["Region", "Subregion", "Country", "Status", "Installation Type"]).agg({"Capacity (MW)": "sum", "Latitude": "mean", "Longitude": "mean", "Start year": lambda x: round(x.dropna().mean()) if not x.dropna().empty else np.nan}).reset_index()
agg_subregion = df.groupby(["Region", "Subregion", "Status", "Installation Type"]).agg({"Capacity (MW)": "sum", "Latitude": "mean", "Longitude": "mean", "Start year": lambda x: round(x.dropna().mean()) if not x.dropna().empty else np.nan}).reset_index()
agg_region = df.groupby(["Region", "Status", "Installation Type"]).agg({"Capacity (MW)": "sum", "Latitude": "mean", "Longitude": "mean", "Start year": lambda x: round(x.dropna().mean()) if not x.dropna().empty else np.nan}).reset_index()

fig = px.scatter_mapbox(df,
                        lat="Latitude",
                        lon="Longitude",
                        size="Capacity (MW)",
                        hover_data=["Capacity (MW)", "Installation Type"],
                        color="Status",
                        zoom=2
                     )

# style=: Allowed values which do not require a Mapbox API token are 'open-street-map', 'white-bg', 'carto-positron',
# 'carto-darkmatter', 'stamen-terrain', 'stamen-toner', 'stamen-watercolor' -> none of them works with available cluster options
# therefore choose between: Allowed values which do require a Mapbox API token are 'basic', 'streets', 'outdoors',
# 'light', 'dark', 'satellite', 'satellite- streets' -> 'light' or 'dark' shows colours of markers best
# if no use of the available cluster options, a style with no need for token can be used like 'carto-positron'
fig.update_layout(mapbox_style="carto-positron")
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
#fig.update_traces(cluster=dict(enabled=True, maxzoom=4, size=12))
fig.update_traces(marker_sizemin=3)

app = Dash()
app.layout = html.Div([
    dcc.Graph(figure=fig)
])

app.run_server(debug=True, use_reloader=False)