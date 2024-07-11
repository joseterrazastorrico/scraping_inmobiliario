import dash
from dash import dcc, html
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px

df = pd.read_csv('./data/data_consolidada_RM.csv')

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
