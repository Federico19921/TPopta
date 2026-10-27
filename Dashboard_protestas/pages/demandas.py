import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

dash.register_page(__name__, path="/demandas", name="Demandas")

df = pd.read_csv("data/eventos.csv")

COLS_DEMANDAS = ["demanda_salarial", "demanda_laboral", "demanda_ambiental_territorial",
                 "demanda_politica_legal", "demanda_ddhh", "demanda_servicios",
                 "demanda_derechos_especificos", "demanda_institucional", "demanda_conmemoracion"]

COLOR_CHUBUT = "#2E86AB"
COLOR_JUJUY = "#A23B72"

def aplicar_estilo(fig):
    fig.update_layout(
        font=dict(family="Arial, sans-serif", size=12, color="#4B5563"),
        plot_bgcolor="white", paper_bgcolor="white",
        margin=dict(l=0, r=0, t=10, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0, title=None),
        xaxis=dict(showgrid=False, showline=False, zeroline=False),
        yaxis=dict(showgrid=True, gridcolor="#F3F4F6", showline=False, zeroline=False)
    )
    return fig

def chart_box(titulo, subtitulo, fig, fuente="Fuente: Base propia de eventos."):
    return html.Div([
        html.Div([html.P(titulo, className="chart-title")], className="chart-header"),
        html.P(subtitulo, className="chart-subtitle"),
        html.Div(dcc.Graph(figure=fig, config={'displayModeBar': False}), className="chart-body"),
        html.Div(fuente, className="chart-footer")
    ], className="chart-container")

demandas = (df.groupby("provincia")[COLS_DEMANDAS].mean() * 100).round(1).T
demandas.columns = ["Chubut", "Jujuy"]
demandas = demandas.sort_values("Jujuy")
demandas.index = [i.replace("demanda_", "").replace("_", " ") for i in demandas.index]
long_dem = demandas.reset_index().melt(id_vars="index", var_name="provincia", value_name="value")

fig_dem = px.bar(long_dem, x="value", y="index", color="provincia", orientation="h", barmode="group",
                 color_discrete_map={"Chubut": COLOR_CHUBUT, "Jujuy": COLOR_JUJUY},
                 labels={"index": "", "value": "% de eventos", "provincia": ""})
fig_dem.update_layout(height=450)
fig_dem = aplicar_estilo(fig_dem)

artic = df.groupby(["provincia", "n_demandas"]).size().reset_index(name="n")
artic["pct"] = artic.groupby("provincia")["n"].transform(lambda x: 100 * x / x.sum())
fig_artic = px.bar(artic, x="n_demandas", y="pct", color="provincia", barmode="group",
                   color_discrete_map={"Chubut": COLOR_CHUBUT, "Jujuy": COLOR_JUJUY},
                   labels={"n_demandas": "Cantidad de demandas por evento", "pct": "% de eventos", "provincia": ""})
fig_artic.update_layout(height=350)
fig_artic = aplicar_estilo(fig_artic)

layout = html.Div([
    html.Div("Inicio | Trabajo e ingresos | Demandas", className="breadcrumbs"),
    html.Div([
        html.H1("Demandas"),
        html.P("Análisis de los reclamos que articulan cada conflicto y su nivel de densidad.", style={"fontSize": "1.1rem", "color": "#4B5563"}),

        html.Div([
            html.H4("Mensajes clave", className="mensajes-clave-title"),
            dbc.Row([
                dbc.Col(html.Div("Jujuy articula un doble eje: político-legal (59,1%) y salarial (59,1%).", className="mensaje-card"), width=4),
                dbc.Col(html.Div("Chubut tiene un eje dominante ambiental-territorial (33,1%) y uno secundario salarial (23,1%).", className="mensaje-card destacado"), width=4),
                dbc.Col(html.Div("Los eventos de Jujuy promedian 1,48 demandas; los de Chubut, 0,95.", className="mensaje-card"), width=4),
            ])
        ], className="mensajes-clave-wrapper"),

        chart_box("Distribución de demandas", "Porcentaje de eventos que incluyen cada tipo de reclamo.", fig_dem),
        chart_box("Articulación de demandas", "Cantidad de demandas superpuestas en un mismo evento.", fig_artic),

        html.Div([
            html.H5("El hallazgo del doble eje"),
            html.P("Los eventos jujeños son eventos densos en términos de demandas; los chubutenses son eventos puros de reclamo único. Esto refleja dos lógicas distintas de organización de la protesta.")
        ], className="hallazgo-box"),

        html.Div([
            dcc.Link("← Volver", href="/repertorios", className="btn btn-outline-secondary"),
            dcc.Link("Siguiente: Cruces →", href="/cruces", className="btn btn-primary float-end"),
        ], style={"marginTop": "40px", "overflow": "hidden"}),
    ], className="page-container")
])