from dash import callback_context
from dash.dependencies import Input, Output
import plotly.express as px

from utils.utils import filter_data


def register_update_map(app, df):
    @app.callback(
        Output('main_map', 'figure'),
        [Input('last_clicked_continent', 'data'),
         Input('sub_region_filter', 'value'),
         Input('country_filter', 'value'),
         Input('status_filter', 'value'),
         Input('type_filter', 'value'),
         Input('time_slider', 'value'),
         Input('main_map', 'relayoutData'),
         Input('bar_chart', 'clickData')]
    )
    def update_map(continent, sub_region, country, status, itype, time_range, zoom_info, clickdata):
        """
        Update the map based on the selected status, time range, and clicked continent.

        Parameters:
        status (list): List of selected statuses.
        time_range (tuple): Start and end year of the selected time range.
        clicked_continent (str): Continent that was last clicked.

        Returns:
        dl.Map: Updated map with markers representing wind farms.
        """
        filtered_df = filter_data(df, continent, sub_region, country, status, itype, time_range)

        agg_country = filtered_df.groupby(["Region", "Subregion", "Country", "Status", "Installation Type"]).agg(
            {"Capacity (MW)": "sum", "Latitude": "mean", "Longitude": "mean",
             "Start year": "mean"}).reset_index()

        if zoom_info and 'mapbox.zoom' in zoom_info:
            zoom_level = zoom_info['mapbox.zoom']
        else:
            zoom_level = 1

        if zoom_level >= 3:
            data = filtered_df  # Filter data based on zoom level
            marker_min = 3
            hover_name = 'Project Name'
            opacity = 0.7
        else:
            data = agg_country
            marker_min = 4
            hover_name = "Country"
            opacity = 1

        # Create a color mapping for the statuses (test based on https://colorbrewer2.org/#type=diverging&scheme=BrBG&n=6)
        color_mapping = {
            'construction': '#5ab4ac',
            'operating': '#01665e',
            'announced': '#d8b365',
            'mothballed': 'lightgrey',
            'cancelled': 'black',
            'pre-construction': '#c7eae5',
            'retired': '#666666',
            'shelved': '#d95f02'
        }

        fig = px.scatter_mapbox(data,
                                lat="Latitude",
                                lon="Longitude",
                                size="Capacity (MW)",
                                hover_name=hover_name,
                                hover_data={"Capacity (MW)": True,
                                            "Installation Type": True,
                                            "Latitude": False,
                                            "Longitude": False},
                                category_orders={'Status': ['operating', 'construction', 'pre-construction', 'announced',
                                                            'retired', 'mothballed', 'shelved', 'cancelled']
                                                 },
                                color="Status",
                                color_discrete_map=color_mapping,
                                zoom=zoom_level,
                                opacity=opacity
                                )

        if zoom_info and 'mapbox.center' in zoom_info:
            fig.update_layout(
                mapbox=dict(
                    center=dict(lat=zoom_info['mapbox.center']['lat'], lon=zoom_info['mapbox.center']['lon']),
                    zoom=zoom_level
                ))

        # style=: Allowed values which do not require a Mapbox API token are 'open-street-map', 'white-bg', 'carto-positron',
        # 'carto-darkmatter', 'stamen-terrain', 'stamen-toner', 'stamen-watercolor' -> none of them works with cluster
        # therefore choose between: Allowed values which do require a Mapbox API token are 'basic', 'streets', 'outdoors',
        # 'light', 'dark', 'satellite', 'satellite- streets' -> 'light' or 'dark' shows colours of markers best
        fig.update_layout(mapbox_style="carto-positron")
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

        fig.update_traces(marker_sizemin=marker_min)

        fig.update_layout(legend=dict(
            yanchor="top",
            y=0.955,
            xanchor="right",
            x=1.2
        ))

        # Center and zoom to clicked project on bar chart
        # TODO: let this only run right after clicking on the bar chart
        if clickdata is not None:
            clicked_project = filtered_df[filtered_df['Project Name'] == clickdata['points'][0]['label']]
            fig.update_layout(mapbox_center_lat=float(clicked_project['Latitude']),
                              mapbox_center_lon=float(clicked_project['Longitude']),
                              mapbox_zoom=7)

        return fig
