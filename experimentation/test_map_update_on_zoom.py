# WORK IN PROGRESS: not yet functioning

from dash import dcc, html, Input, Output, Dash
import plotly.graph_objs as go
import pandas as pd

# Sample data
df = pd.DataFrame({
    'latitude': [40.7128, 34.0522, 41.8781, 29.7604, 37.7749],
    'longitude': [-74.0060, -118.2437, -87.6298, -95.3698, -122.4194],
    'text': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'San Francisco'],
    'zoom_level_threshold': [5, 6, 7, 8, 9]  # Thresholds for different zoom levels
})

app = Dash(__name__)

@app.callback(
    Output('map-graph', 'figure'),
    [Input('map-graph', 'relayoutData')]
)
def update_on_zoom(relayoutData):
    if relayoutData is None or 'mapbox' not in relayoutData:
        zoom_level = 3  # Default zoom level
    else:
        zoom_level = relayoutData['mapbox']['zoom']

    new_data = df[df['zoom_level_threshold'] <= zoom_level]  # Filter data based on zoom level

    fig = go.Figure(go.Scattermapbox(
        lat=new_data['latitude'],
        lon=new_data['longitude'],
        mode='markers',
        marker=dict(size=10),
        text=new_data['text']
    ))

    fig.update_layout(
        hovermode='closest',
        mapbox=dict(
            style='open-street-map',
            center=dict(lat=38, lon=-94),
            zoom=zoom_level
        )
    )

    return fig

app.layout = html.Div([
    dcc.Graph(id='map-graph')
])

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)