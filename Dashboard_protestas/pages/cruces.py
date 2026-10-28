import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

dash.register_page(__name__, path="/cruces", name="Cruces")

df = pd.read_csv("data/eventos.csv")

COLS_ACTORES = ["docentes", "gremios_estatales", "sindicatos_privados", "organizaciones_sociales",
                "comunidades_indigenas", "vecinos", "colectivos_ambientales", "colectivos_especificos",
                "partidos_politicos", "policias_actores", "publico_general", "colectivos_violentos"]
COLS_DEMANDAS = ["demanda_salarial", "demanda_laboral", "demanda_ambiental_territorial", "demanda_politica_legal",
                 "demanda_ddhh", "demanda_servicios", "demanda_derechos_especificos", "demanda_institucional", "demanda_conmemoracion"]

LABELS_ACTORES = {"docentes": "Docentes", "gremios_estatales": "Gremios estatales", "sindicatos_privados": "Sindicatos privados",
                  "organizaciones_sociales": "Org. sociales", "comunidades_indigenas": "Comunidades indígenas", "vecinos": "Vecinos",
                  "colectivos_ambientales": "Colectivos ambientales", "colectivos_especificos": "Colectivos específicos",
                  "partidos_politicos": "Partidos políticos", "policias_actores": "Policías", "publico_general": "Público general",
                  "colectivos_violentos": "Colectivos violentos"}
LABELS_DEMANDAS = {"demanda_salarial": "Salarial", "demanda_laboral": "Laboral", "demanda_ambiental_territorial": "Ambiental",
                   "demanda_politica_legal": "Política", "demanda_ddhh": "DDHH", "demanda_servicios": "Servicios",
                   "demanda_derechos_especificos": "Dchos. específicos", "demanda_institucional": "Institucional", "demanda_conmemoracion": "Conmemoración"}

def aplicar_estilo(fig):
    fig.update_layout(
        font=dict(family="Arial, sans-serif", size=12, color="#4B5563"),
        plot_bgcolor="white", paper_bgcolor="white", margin=dict(l=0, r=0, t=20, b=40),
        xaxis=dict(showgrid=False, showline=False, zeroline=False),
        yaxis=dict(showgrid=True, gridcolor="#F3F4F6", showline=False, zeroline=False)
    )
    return fig

def construir_matriz(sub):
    matriz = pd.DataFrame(0, index=list(LABELS_ACTORES.values()), columns=list(LABELS_DEMANDAS.values()))
    for _, row in sub.iterrows():
        actores = [LABELS_ACTORES[a] for a in COLS_ACTORES if row[a] == 1]
        demandas = [LABELS_DEMANDAS[d] for d in COLS_DEMANDAS if row[d] == 1]
        for a in actores:
            for d in demandas:
                matriz.loc[a, d] += 1
    return matriz.loc[matriz.sum(axis=1) > 0, matriz.sum(axis=0) > 0]

# Calcular matrices
ch = construir_matriz(df[df["provincia"] == "Chubut"])
ju = construir_matriz(df[df["provincia"] == "Jujuy"])

todas_act = sorted(set(ch.index) | set(ju.index))
todas_dem = sorted(set(ch.columns) | set(ju.columns))
ch = ch.reindex(index=todas_act, columns=todas_dem, fill_value=0)
ju = ju.reindex(index=todas_act, columns=todas_dem, fill_value=0)

fig_matriz = make_subplots(rows=1, cols=2, subplot_titles=("Chubut", "Jujuy"), shared_yaxes=True, horizontal_spacing=0.08)
fig_matriz.add_trace(go.Heatmap(z=ch.values, x=todas_dem, y=todas_act, colorscale="Blues", showscale=False,
                                text=ch.values, texttemplate="%{text}", textfont={"size": 9}), row=1, col=1)
fig_matriz.add_trace(go.Heatmap(z=ju.values, x=todas_dem, y=todas_act, colorscale="Reds", showscale=False,
                                text=ju.values, texttemplate="%{text}", textfont={"size": 9}), row=1, col=2)
fig_matriz.update_layout(height=550, margin=dict(l=160, r=20, t=60, b=140))
fig_matriz.update_xaxes(tickangle=-45)
fig_matriz = aplicar_estilo(fig_matriz)

layout = html.Div([
    html.Div("Inicio | Trabajo e ingresos | Cruces", className="breadcrumbs"),
    html.Div([
        html.H1("Cruce de actores y demandas"),
        html.P("Análisis de qué actores sostienen qué reclamos en cada conflicto.", style={"fontSize": "1.1rem", "color": "#4B5563"}),

        html.Div([
            html.H4("Mensajes clave", className="mensajes-clave-title"),
            dbc.Row([
                dbc.Col(html.Div("En Jujuy, los docentes y las organizaciones sociales concentran las demandas políticas y salariales.", className="mensaje-card"), width=6),
                dbc.Col(html.Div("En Chubut, los vecinos y los colectivos ambientales son el núcleo de la demanda territorial.", className="mensaje-card destacado"), width=6),
            ])
        ], className="mensajes-clave-wrapper"),

        html.Div([
            html.Div([html.P("Matriz Actor × Demanda", className="chart-title")], className="chart-header"),
            html.P("Cantidad de eventos donde coexisten un actor y una demanda. Azul: Chubut, Rojo: Jujuy.", className="chart-subtitle"),
            html.Div(dcc.Graph(figure=fig_matriz, config={'displayModeBar': False}), className="chart-body"),
            html.Div("Fuente: Base propia de eventos.", className="chart-footer")
        ], className="chart-container"),

        html.Div([
            html.H5("El cruce de actores y demandas"),
            html.P("Mientras que en Chubut el reclamo territorial (ambiental) es sostenido principalmente por vecinos y colectivos ambientales, en Jujuy los docentes son el actor protagónico que articula demandas salariales y políticas. Las comunidades indígenas, por su parte, sostienen demandas de derechos específicos y territoriales.")
        ], className="hallazgo-box"),

        html.Div([
            dcc.Link("← Volver", href="/demandas", className="btn btn-outline-secondary"),
            dcc.Link("Siguiente: Represión →", href="/represion", className="btn btn-primary float-end"),
        ], style={"marginTop": "40px", "overflow": "hidden"}),
    ], className="page-container")
])