from dash.dependencies import Input, Output

from utils.utils import filter_data


def register_update_status_filter(app, df):
    @app.callback(
        Output("status_filter", 'options'),
        [Input('last_clicked_continent', 'data'),
        Input("sub_region_filter", "value"),
        Input("country_filter", "value"),
        Input("type_filter", "value"),
        Input("time_slider", "value")]
    )
    def update_subregion_filter(continent, sub_region, country, itype, time_range):
        """
        Updates the available options in the type dropdown when any filter option has been clicked
        Returns:
            a list of (string) type values
        """
        filtered_df = filter_data(df, continent, sub_region, country, None, itype, time_range)
        options = filtered_df["Status"].unique()
        return options


def register_update_type_filter(app, df):
    @app.callback(
        Output("type_filter", 'options'),
        [Input('last_clicked_continent', 'data'),
         Input("sub_region_filter", "value"),
         Input("country_filter", "value"),
         Input("status_filter", "value"),
         Input("time_slider", "value")]
    )
    def update_subregion_filter(continent, sub_region, country, status, time_range):
        """
        Updates the available options in the type dropdown when any filter option has been clicked
        Returns:
            a list of (string) type values
        """
        filtered_df = filter_data(df, continent, sub_region, country, status, None, time_range)
        options = filtered_df["Installation Type"].unique()
        return options
