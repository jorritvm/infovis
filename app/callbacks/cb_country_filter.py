from dash.dependencies import Input, Output


def register_update_country_filter(app, agg):
    @app.callback(
        Output("country_filter", "options"),
        Input("sub_region_filter", "value")
    )
    def update_country_filter(sub_region):
        """
        Updates the available options in the country dropdown when the subregion filter has been selected
        Args:
            sub_region: string specifying a subregion
        Returns:
            list of (string) countries in this subregion
        """
        if sub_region == "" or sub_region is None:
            return []
        else:
            countries = agg[agg["Subregion"] == sub_region]["Country"].unique()
            return countries