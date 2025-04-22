# Dashboard
import dash
from dash import Dash, html, dcc, Input, Output, callback
import plotly.express as px
import pandas as pd

from graficar import plotbar,plotpiechar,plotmap


# Datos de ejemplo (usa tus datos reales)
data = {
    'City': ['San Antonio', 'Los Angeles', 'Houston', 'Phoenix', 'New York', 'San Diego', 'Chicago', 'Philadelphia'],
    'TotalSales': [160649778748, 137201744784, 65184223598, 61687874548, 53988050104, 48027313176, 40831923628, 37644422096],
    'MeanSales': [1.254097e+08, 1.192022e+08, 8.543149e+07, 1.177250e+08, 8.542413e+07, 7.492561e+07, 7.959439e+07, 1.459086e+08],
    'cv': [54.13, 39.93, 74.73, 33.85, 47.71, 36.53, 56.71, 34.74],
    'Latitude': [29.4241, 34.0522, 29.7604, 33.4484, 40.7128, 32.7157, 41.8781, 39.9526],
    'Longitude': [-98.4936, -118.2437, -95.3698, -112.0740, -74.0060, -117.1611, -87.6298, -75.1652]
}
dataset = pd.DataFrame(data)
dataset['TotalSales'] = dataset['TotalSales']/1e9
dataset['MeanSales'] = dataset['MeanSales']/1e6


# Inicializar la app Dash
app = Dash(__name__)

app.layout = html.Div([
    # Primera fila: Pie chart y Bar chart
    html.Div([
        html.Div([
            dcc.Graph(
                id='pie-chart', 
                config={'displayModeBar': False},
                style={
                    'border': '1px solid #cccccc',
                    'borderRadius': '8px',
                    'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
                    'height': '300px'  # Asegura que ocupe todo el espacio del contenedor
                }
            )
        ], style={
            'width': '48%',  # Reducimos ligeramente el ancho para dejar más espacio al margen
            'display': 'inline-block',
            'verticalAlign': 'top',
            'padding': '10px',
            'margin': '5px',
            'backgroundColor': '#ffffff',
            'borderRadius': '8px',
            'boxShadow': '0 1px 3px rgba(0,0,0,0.1)'
        }),

        html.Div([
            dcc.Graph(
                id='bar-chart-cv', 
                config={'displayModeBar': False},
                style={
                    'border': '1px solid #cccccc',
                    'borderRadius': '8px',
                    'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
                    'height': '300px'
                }
            )
        ], style={
            'width': '48%',
            'display': 'inline-block',
            'verticalAlign': 'top',
            'padding': '10px',
            'margin': '5px',
            'backgroundColor': '#ffffff',
            'borderRadius': '8px',
            'boxShadow': '0 1px 3px rgba(0,0,0,0.1)'
        })
    ], style={
        'marginBottom': '10px',
        'display': 'flex',
        'justifyContent': 'space-between'
    }),

    # Segunda fila: Mapa y gráfico de promedio de ventas alineados
    html.Div([
        html.Div([
            dcc.Graph(
                id='city-map', 
                config={'displayModeBar': False},
                style={
                    'border': '1px solid #cccccc',
                    'borderRadius': '8px',
                    'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
                    'height': '300px'
                }
            )
        ], style={
            'width': '48%',
            'display': 'inline-block',
            'verticalAlign': 'top',
            'padding': '10px',
            'margin': '5px',
            'backgroundColor': '#ffffff',
            'borderRadius': '8px',
            'boxShadow': '0 1px 3px rgba(0,0,0,0.1)'
        }),

        html.Div([
            dcc.Graph(
                id='bar-chart-salesmean', 
                config={'displayModeBar': False},
                style={
                    'border': '1px solid #cccccc',
                    'borderRadius': '8px',
                    'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
                    'height': '300px'
                }
            )
        ], style={
            'width': '48%',
            'display': 'inline-block',
            'verticalAlign': 'top',
            'padding': '10px',
            'margin': '5px',
            'backgroundColor': '#ffffff',
            'borderRadius': '8px',
            'boxShadow': '0 1px 3px rgba(0,0,0,0.1)'
        })
    ], style={
        'marginTop': '10px',
        'display': 'flex',
        'justifyContent': 'space-between'
    })
], style={
    'maxWidth': '1200px', 
    'margin': '20px auto', 
    'padding': '15px',
    'backgroundColor': '#f5f5f5',
    'borderRadius': '10px'
})




# Inicializamos la variable para recordar la ciudad seleccionada

# Crear y actualizar los gráficos estáticos iniciales
@app.callback(
    [Output('pie-chart', 'figure'),
    Output('bar-chart-cv', 'figure'),
    Output('city-map', 'figure'),
    Output('bar-chart-salesmean','figure')],
    [Input('pie-chart', 'clickData'),
    Input('bar-chart-cv', 'clickData'),
    Input('city-map', 'clickData'),
    Input('bar-chart-salesmean', 'clickData')]
)
def update_graphs(pie_click, bar_cv_click, map_click, bar_sales_click):
    # Detectar la ciudad seleccionada al hacer clic en cualquiera de los gráficos (pie chart, barras o mapa).
    # También maneja la lógica de selección/deselección para permitir alternar la ciudad seleccionada.
    if not hasattr(update_graphs, 'last_city'):
        update_graphs.last_city = None

    ctx = dash.callback_context
    selected_city = None

    if ctx.triggered:
        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
        click_data = ctx.triggered[0]['value']

        if click_data and 'points' in click_data and len(click_data['points']) > 0:
            point = click_data['points'][0]
            
            # Intentamos extraer la ciudad desde diferentes claves posibles
            if triggered_id == 'pie-chart':
                selected_city = point.get('label')
            elif triggered_id in ['bar-chart-cv', 'bar-chart-salesmean']:
                selected_city = point.get('y') or point.get('label') or point.get('customdata')
            elif triggered_id == 'city-map':
                selected_city = point.get('hovertext')

    # Comparar con la última ciudad seleccionada (normalizando)
    selected_city_norm = selected_city.strip().lower() if selected_city else None
    last_city_norm = update_graphs.last_city.strip().lower() if update_graphs.last_city else None

    if selected_city_norm == last_city_norm:
        selected_city = None
        update_graphs.last_city = None
    else:
        update_graphs.last_city = selected_city

    # Pie chart
    pie_fig, pie_colors = plotpiechar(dataset,names ='City',values='TotalSales',
                                    labels={'TotalSales': 'Ventas'},
                                    hovertemplate='<b>%{label}</b><br>Ventas: %{value:.0f} mil M<extra></extra>',  # Formato con un decimal al pasar el mouse
                                    texttemplate='%{value:.0f}mil M',  # Formato con un decimal dentro de las porciones,
                                    title='Ventas por ciudad')

    # Bar chart CV
    bar_fig = plotbar(dataset,pie_colors,Y ='City',X='cv',
                    Labels={'cv': 'Porcentaje de variación'},
                    texttemplate ='<b>%{x:.2f}%</b>', # muestra 2 decimales y el simbolo %
                    Title=''

                    )
    
    # Bar chart ventas promedio
    bar_figm = plotbar(dataset,pie_colors,Y ='City',X='MeanSales',
                    Labels={'MeanSales': 'Ventas Promedio ($)'},
                    texttemplate ='<b>%{x:.2f}M</b>', # muestra 2 decimales y el simbolo %
                    Title='')

    # Mapa
    map_fig = plotmap(dataset,pie_colors,mapbox_style="open-street-map")

    # Efectos visuales si hay selección
    if selected_city:
        selected_data = dataset[dataset['City'] == selected_city].iloc[0]
        map_fig.update_layout(
            mapbox_zoom=8,
            mapbox_center={"lat": selected_data['Latitude'], "lon": selected_data['Longitude']}
        )

        for barra in bar_fig.data:
            barra.opacity = 1.0 if barra.name == selected_city else 0.2

        for barra in bar_figm.data:
            barra.opacity = 1.0 if barra.name == selected_city else 0.2

        labels = pie_fig.data[0]['labels']
        pulls = [0.05 if label == selected_city else 0 for label in labels]
        pie_fig.data[0].pull = pulls
    else:
        pie_fig.data[0].pull = [0] * len(pie_fig.data[0]['labels'])
        for barra in bar_fig.data:
            barra.opacity = 1.0
        for barra in bar_figm.data:
            barra.opacity = 1.0

    return pie_fig, bar_fig, map_fig, bar_figm

if __name__ == '__main__':
    app.run(debug=True, port=8052)