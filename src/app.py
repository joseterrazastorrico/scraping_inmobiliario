import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import geopandas as gpd
import dash_table
import folium
import unicodedata

df = pd.read_csv('./data/consolidated_properties/data_consolidada_RM.csv', index_col=0)
df['comuna'] = df['comuna'].str.split('-').apply(lambda x: ' '.join([word.capitalize() for word in x]))
df['comuna'] = df['comuna'].apply(lambda x: unicodedata.normalize('NFKD', x).encode('ASCII', 'ignore').decode('utf-8'))
df = df.loc[df.proyecto==False]

comunas_geo = gpd.read_file('./data/maps/division_comunal.geojson')
comunas_geo['NOM_COM'] = comunas_geo['NOM_COM'].apply(lambda x: unicodedata.normalize('NFKD', x).encode('ASCII', 'ignore').decode('utf-8'))
comunas_geo = comunas_geo.merge(df.groupby('comuna').mean().reset_index(), left_on='NOM_COM', right_on='comuna')

# Crear la aplicación Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout de la aplicación
app.layout = dbc.Container([
    # Título principal
    html.H1("Análisis de Propiedades en la Región Metropolitana", className="text-center mt-4 mb-4"),

    # Sección 1: Mapa
    html.Div([
        html.H2("Mapa de Comunas", className="mb-3"),
        dbc.Row([
            dbc.Col([
                html.Label('Selecciona una variable:'),
                dcc.Dropdown(
                    id='variable-dropdown',
                    options=[{'label': col, 'value': col} for col in df.columns],
                    value='price_clean_uf',
                )
            ], width=4),
            dbc.Col([
                html.Div(id='mapa-comunas'),
            ], width=8)
        ])
    ], className="mb-5"),

    # Sección 2: Tabla de resumen y scatterplots
    html.Div([
        html.H2("Resumen de Propiedades", className="mb-3"),
        dbc.Row([
            dbc.Col([
                html.Label('Selecciona una comuna:'),
                dcc.Dropdown(
                    id='comuna-dropdown',
                    options=[{'label': comuna, 'value': comuna} for comuna in df['comuna'].unique()],
                    value=df['comuna'].unique()[0]
                ),
                html.Label('Cantidad de piezas:'),
                dcc.Dropdown(
                    id='piezas-dropdown',
                    options=[{'label': str(piezas), 'value': piezas} for piezas in sorted(df['dormitorios_clean'].unique())],
                    value=sorted(df['dormitorios_clean'].unique())[0]
                )
            ], width=4),
            dbc.Col([
                html.H4('Tabla de propiedades filtradas'),
                dash_table.DataTable(
                                id='tabla-propiedades',
                                columns=[{"name": i, "id": i} for i in df.columns],
                                data=df.to_dict('records'),
                                style_table={'overflowX': 'auto'},
                                style_cell={'textAlign': 'left'},
                                page_size=10
                            ),
            ], width=8)
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Graph(id='grafico-promedio')
            ], width=12)
        ])
    ])
])


# Callbacks
@app.callback(
    Output('mapa-comunas', 'children'),
    Input('variable-dropdown', 'value')
)
def update_map(selected_column):
    # Crear el mapa con la columna seleccionada
    m = folium.Map(location=[-33.45, -70.65], zoom_start=10)

    # Añadir las comunas coloreadas con información en hover
    folium.Choropleth(
        geo_data=comunas_geo,
        data=comunas_geo,
        columns=['comuna', selected_column],
        key_on='feature.properties.NOM_COM',
        fill_color='YlOrRd',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name=f'{selected_column} por comuna'
    ).add_to(m)

    # Añadir tooltips para mostrar información al pasar el mouse
    for _, row in comunas_geo.iterrows():
        folium.GeoJson(
            row['geometry'],
            tooltip=folium.Tooltip(f"{row['comuna']}: {row[selected_column]}")
        ).add_to(m)

    # Guardar el mapa en un archivo temporal y leerlo
    map_file = 'map.html'
    m.save(map_file)

    return html.Iframe(srcDoc=open(map_file, 'r').read(), style = {'width': '100%', 'height': '600px'})

@app.callback(
    [Output('tabla-propiedades', 'data'),
     Output('grafico-promedio', 'figure')],
    [Input('comuna-dropdown', 'value'),
     Input('piezas-dropdown', 'value')]
)
def actualizar_tabla_grafico(comuna, piezas):
    filtrado = df[(df['comuna'] == comuna) & (df['dormitorios_clean'] == piezas)]
    # Gráfico de promedio
    grafico = px.bar(df.groupby('comuna').mean().reset_index(), x='comuna', y='price_clean_uf',
                     title='Promedio de precios por comuna')
    return filtrado.to_dict('records'), grafico

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run_server(port=8055, debug=True)
