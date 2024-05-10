import dash
from dash.dependencies import Input, Output


def register_update_country_filter(app, agg, continents):
    @app.callback(
        Output("country_filter", "options"),
        Input("sub_region_filter", "value"),
        [Input(f"{continent}_click", 'n_clicks') for continent in continents]
    )
    def update_country_filter(sub_region, *args):
        """
        Updates the available options in the country dropdown when the subregion filter has been selected
        Args:
            sub_region: string specifying a subregion
        Returns:
            list of (string) countries in this subregion
        """
        # Get the ID of the triggering input
        ctx = dash.callback_context
        triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]

        if triggered_id == "sub_region_filter":
            if sub_region == "" or sub_region is None or sub_region == []:
                return []
            else:
                countries = agg[agg["Subregion"] == sub_region]["Country"].unique()
            return countries
        else:
            return []


def register_reset_country(app, continents):
    @app.callback(
        Output("country_filter", 'value'),
        [Input(f"{continent}_click", 'n_clicks') for continent in continents]
    )
    def reset_country(*button_clicks):
        return None
