import dash
from dash import dcc, html
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
import plotly.express as px




app = dash.Dash(__name__)

fig_m2 = px.histogram(df, x='m2', title='Distribución de m2')
fig_precio = px.histogram(df, x='price', title='Distribución de Precios')
fig_habitaciones = px.histogram(df, x='dormitorios', title='Distribución de Habitaciones')
fig_baños = px.histogram(df, x='banos', title='Distribución de Baños')

# Diseñar el layout del dashboard
app.layout = html.Div(children=[
    html.H1(children='Dashboard de Propiedades'),

    html.Div(children='''
        Visualización de datos de propiedades.
    '''),

    dcc.Graph(
        id='m2-graph',
        figure=fig_m2
    ),

    dcc.Graph(
        id='precio-graph',
        figure=fig_precio
    ),

    dcc.Graph(
        id='habitaciones-graph',
        figure=fig_habitaciones
    ),

    dcc.Graph(
        id='baños-graph',
        figure=fig_baños
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)

# app.py
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

df = pd.read_csv('./data/data_consolidada_RM.csv')
df = df.loc[df.proyecto==False]

# Crear la aplicación Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout de la aplicación
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.Label('Selecciona una variable:'),
            dcc.Dropdown(
                id='variable-dropdown',
                options=[{'label': col, 'value': col} for col in df.columns],
                value='price_clean_uf'
            )
        ], width=4),
        dbc.Col([
            dcc.Graph(id='mapa-comunas')
        ], width=8)
    ]),
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
            dcc.Graph(id='tabla-propiedades')
        ], width=8)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='grafico-promedio')
        ], width=12)
    ])
])

# Callbacks
@app.callback(
    Output('mapa-comunas', 'figure'),
    Input('variable-dropdown', 'value')
)
def actualizar_mapa(variable):
    fig = px.choropleth(df, geojson='santiago.json', locations='comuna', color=variable,
                        featureidkey="properties.COMUNA")  # Asegúrate de tener un archivo geojson con los datos geográficos de Santiago
    fig.update_geos(fitbounds="locations", visible=False)
    return fig

@app.callback(
    [Output('tabla-propiedades', 'figure'),
     Output('grafico-promedio', 'figure')],
    [Input('comuna-dropdown', 'value'),
     Input('piezas-dropdown', 'value')]
)
def actualizar_tabla_grafico(comuna, piezas):
    filtrado = df[(df['comuna'] == comuna) & (df['dormitorios_clean'] == piezas)]
    
    # Tabla de propiedades
    tabla = px.scatter(filtrado, x='direccion', y='price_clean_uf', title='Propiedades filtradas')
    
    # Gráfico de promedio
    promedio = filtrado.groupby('comuna').mean().reset_index()
    grafico = px.bar(promedio, x='comuna', y='precio', title='Promedio de precios por comuna')
    
    return tabla, grafico

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)
