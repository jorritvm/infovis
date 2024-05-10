import dash
from dash.dependencies import Input, Output

from utils.utils import filter_data


def register_update_clicked_continent(app, continents):
    @app.callback(
        Output('last_clicked_continent', 'data'),
        [Input(f"{continent}_click", 'n_clicks') for continent in continents]
    )
    def update_clicked_continent(*continent_clicks):
        """
        Update the data (dcc.store value) for the last clicked continent.

        Parameters:
        *continent_clicks: Variable number of input arguments representing the number of clicks for each continent.

        Returns:
        The name of the last clicked continent if a button was clicked, otherwise returns "Total".
        """
        ctx = dash.callback_context
        if ctx.triggered:
            button_id = ctx.triggered[0]['prop_id'].split('.')[0]
            clicked_continent = button_id.replace("_click", "")
            return clicked_continent
        else:
            return "Total"


def register_update_capacities(app, continents, df):
    @app.callback(
        [Output(f"{continent}_capacity", 'children') for continent in continents],
        [Input('status_filter', 'value'),
         Input('type_filter', 'value'),
         Input('time_slider', 'value')]
    )
    def update_capacities_on_cards(status, itype, time_range):
        """
        Updates the values on the BAN's when the status dropdown or time_range has been modified
        Args:
            status: string
            time_range: tuple of (start_year, end_year)
        Returns:
            A list of strings, representing the capacities per continent
        """
        dfx = filter_data(df, "Total", None, None, status, itype, time_range)

        # make output values for every continent
        output_capacities = []
        for continent in continents:
            if continent == "Total":
                capa = dfx["Capacity (MW)"].sum()
            else:
                capa = dfx[dfx["Region"] == continent]["Capacity (MW)"].sum()
            output_capacities = output_capacities + [capa]

        # format output
        output_capacities = [round(x) for x in output_capacities]  # round
        output_capacities = [f"{x:,}" for x in output_capacities]  # put thousand sep ,
        output_capacities = [x.replace(",", ".") for x in output_capacities]  # put thousand sep .
        output_capacities = [f"{x} MW" for x in output_capacities]  # adding the SI unit .
        return output_capacities


def register_update_ban_style(app, continents):
    # Define a callback to update the button style based on the last clicked continent
    @app.callback(
        [Output(f"{continent}_click", 'color') for continent in continents],
        [Input('last_clicked_continent', 'data')]
    )
    def update_ban_style(last_clicked_continent):
        """
        Darkens the BAN that you have clicked on to show it has been selected

        Parameters:
        last_clicked_continent: string representing the currently active continent filter

        Returns:
        a list of color values for all the continent buttons 'color' prop
        """
        result = []
        for continent in continents:
            if continent == last_clicked_continent:
                result.append("info")
            else:
                result.append("secondary")
        return result
