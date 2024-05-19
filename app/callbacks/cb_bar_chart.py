from dash import callback_context
from dash.dependencies import Input, Output
import plotly.express as px

from utils.utils import filter_data

def register_update_bar_chart(app, df):
    @app.callback(
        Output('bar_chart', 'figure'),
        [Input('last_clicked_continent', 'data'),
         Input('sub_region_filter', 'value'),
         Input('country_filter', 'value'),
         Input('status_filter', 'value'),
         Input('type_filter', 'value'),
         Input('time_slider', 'value'),
         ]
    )
    def update_bar_chart(continent, sub_region, country, status, itype, time_range):
        """
        Updates the plotly bar chart when the user modifies the status filter, time slider or clicks on another continent
        Args:
            status: list of selected status strings
            time_range: tuple of 2 integers (start & end year)
            continent: string value for last clicked continent
        Returns:
            plotly figure to update the bar chart
        """
        # filter the whole dataset
        # print("filtering for bar chart")
        dfx = filter_data(df, continent, sub_region, country, status, itype, time_range)
        # aggregate onto project level: combine project phases and statuses
        dfx_agg = dfx.groupby(["Region", "Subregion", "Country", "Installation Type", "Project Name", "Status"]).agg(
            {"Capacity (MW)": "sum", "Latitude": "mean", "Longitude": "mean",
             "Start year": "mean"}).reset_index()
        # Sort DataFrame by capacity in descending order and select top 20 wind farms
        top_20 = dfx_agg.nlargest(20, "Capacity (MW)")
        top_20 = top_20.sort_values("Capacity (MW)")
        # Create horizontal bar chart
        color_mapping = {
            'operating': '#1b9e77',
            'future': '#7570b3',
            'retired': '#d95f02',
        }
        fig = px.bar(top_20,
                     x='Capacity (MW)',
                     y='Project Name',
                     orientation='h',
                     color='Status',
                     color_discrete_map=color_mapping,
                     hover_data=['Region', 'Subregion', 'Country',
                                 'Project Name', 'Capacity (MW)'],
                     title="Top 20 Largest Wind Farms"
                     )
        fig.update_layout(
            showlegend=False,
            legend=dict(
                orientation="h",
                yanchor="top",
                y=-0.2,
                xanchor="right",
                x=1
            ),
            yaxis=dict(
                categoryorder='total ascending'
            ), 
            autosize=False,
            margin=dict(
                l=220,
                r=5,  # right margin
                b=100,  # bottom margin
                t=100,  # top margin
                ),
                title_x=0.5,  # title position
                annotations=[
                    dict(
                        x=-2,  # x position
                        y=-0.15,  # y position
                        showarrow=False,
                        text="Capacity (MW)",  # annotation text
                        xref="paper",
                        yref="paper",
                        font=dict(size=14)
                    )
                ]
        )
        fig.update_yaxes(
            title=None,
            tickfont=dict(
                size=10,
            ),
        )
        fig.update_xaxes(title=None)
        return fig