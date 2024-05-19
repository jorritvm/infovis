import dash
from dash.dependencies import Input, Output


def register_update_subregion_filter(app, continents, agg):
    @app.callback(
        Output("sub_region_filter", 'options'),
        [Input(f"{continent}_click", 'n_clicks') for continent in continents]
    )
    def update_subregion_filter(*button_clicks):
        """
        Updates the available options in the subregion dropdown when the region BAN has been clicked
        Args:
            *button_clicks: not used
        Returns:
            a list of (string) sub region values and an empty list for the countries
        """
        options = []
        ctx = dash.callback_context
        if ctx.triggered:
            button_id = ctx.triggered[0]['prop_id'].split('.')[0]
            continent = button_id.replace("_click", "")
            options = []
            if continent != "Total":
                options = agg[agg["Region"] == continent]["Subregion"].unique()
        return options



def register_reset_subregion(app, continents):
    @app.callback(
        Output("sub_region_filter", 'value'),
        [Input(f"{continent}_click", 'n_clicks') for continent in continents]
    )
    def reset_subregion(*button_clicks):
        """
        Clears the currently selected 'sub region' value when a continent is clicked
        """
        return None

