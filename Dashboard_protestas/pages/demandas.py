import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

dash.register_page(__name__, path="/demandas", name="Demandas")

df = pd.read_csv("data/eventos.csv")

COLS_DEMANDAS = ["demanda_salarial", "demanda_laboral", "demanda_ambiental_territorial",
                 "demanda_politica_legal", "demanda_ddhh", "demanda_servicios",
                 "demanda_derechos_especificos", "demanda_institucional",
                 "demanda_conmemoracion"]

COLOR_CHUBUT = "#2E86AB"
COLOR_JUJUY = "#A23B72"

def aplicar_estilo(fig):
    fig.update_layout(
        font=dict(family="Inter, sans-serif", size=12, color="#374151"),
        title=dict(font=dict(size=14, color="#151515"), x=0, xanchor="left"),
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=40, r=20, t=50, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.02,
                    xanchor="right", x=1, font=dict(size=11)),
        xaxis=dict(showgrid=False, linecolor="#E5E7EB"),
        yaxis=dict(gridcolor="#E5E7EB", gridwidth=0.5),
        hoverlabel=dict(bgcolor="white")
    )
    return fig

demandas = (df.groupby("provincia")[COLS_DEMANDAS].mean() * 100).round(1).T
demandas.columns = ["Chubut", "Jujuy"]
demandas = demandas.sort_values("Jujuy")
demandas.index = [i.replace("demanda_", "").replace("_", " ") for i in demandas.index]

fig_dem = px.bar(
    demandas.reset_index().melt(id_vars="index", var_name="provincia", value_name="value"),
    x="value", y="index", color="provincia",
    orientation="h", barmode="group",
    color_discrete_map={"Chubut": COLOR_CHUBUT, "Jujuy": COLOR_JUJUY},
    labels={"index": "", "value": "% de eventos", "provincia": ""},
    title="Demandas por provincia"
)
fig_dem.update_layout(height=500)
fig_dem = aplicar_estilo(fig_dem)

artic = df.groupby(["provincia", "n_demandas"]).size().reset_index(name="n")
artic["pct"] = artic.groupby("provincia")["n"].transform(lambda x: 100 * x / x.sum())

fig_artic = px.bar(
    artic, x="n_demandas", y="pct", color="provincia", barmode="group",
    color_discrete_map={"Chubut": COLOR_CHUBUT, "Jujuy": COLOR_JUJUY},
    labels={"n_demandas": "Cantidad de demandas por evento",
            "pct": "% de eventos", "provincia": ""},
    title="Articulación de demandas"
)
fig_artic.update_layout(height=400)
fig_artic = aplicar_estilo(fig_artic)

layout = html.Div([
    html.H1("Demandas"),
    html.P("Qué se reclamó y cómo se articuló en cada conflicto.",
           className="text-muted mb-4"),

    html.H2("Distribución de demandas"),
    html.P("Jujuy articula un doble eje con igual peso (político-legal y salarial). "
           "Chubut tiene un eje dominante (ambiental-territorial) con un secundario (salarial).",
           className="text-muted"),
    dcc.Graph(figure=fig_dem),

    html.H2("Articulación de demandas"),
    html.P("El 47% de los eventos de Jujuy tienen dos o más demandas. "
           "En Chubut, la mayoría tiene una sola.",
           className="text-muted"),
    dcc.Graph(figure=fig_artic),

    html.Div([
        html.H5("Hallazgo: doble eje vs eje dominante"),
        html.P("El promedio de demandas por evento es 1,48 en Jujuy y 0,95 en Chubut. "
               "Los eventos jujeños son eventos densos en términos de demandas; "
               "los chubutenses son eventos puros de reclamo único.")
    ], className="hallazgo-box"),

    html.Div([
        dcc.Link("← Volver", href="/repertorios", className="btn btn-outline-secondary"),
        dcc.Link("Siguiente: Cruces →", href="/cruces",
                 className="btn btn-primary float-end"),
    ], style={"marginTop": "32px", "overflow": "hidden"}),

], className="page-container")