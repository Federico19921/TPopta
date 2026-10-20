import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

dash.register_page(__name__, path="/repertorios", name="Repertorios")

df = pd.read_csv("data/eventos.csv")

COLS_ACCION = ["tiene_marcha", "tiene_corte", "tiene_paro", "tiene_acto",
               "tiene_escrache", "tiene_destrozos", "tiene_toma"]

COLS_ACTORES = ["docentes", "gremios_estatales", "sindicatos_privados",
                "organizaciones_sociales", "comunidades_indigenas", "vecinos",
                "colectivos_ambientales", "colectivos_especificos",
                "partidos_politicos", "policias_actores",
                "publico_general", "colectivos_violentos"]

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

layout = html.Div([
    html.H1("Repertorios y actores"),
    html.P("Qué se hizo y quiénes lo hicieron en cada conflicto.",
           className="text-muted mb-4"),

    dcc.Tabs(id="tabs-rep", value="tab-acciones", className="tab-parent", children=[
        dcc.Tab(label="Repertorios", value="tab-acciones", className="tab",
                selected_className="tab--selected"),
        dcc.Tab(label="Actores", value="tab-actores", className="tab",
                selected_className="tab--selected"),
        dcc.Tab(label="Densidad del evento", value="tab-densidad", className="tab",
                selected_className="tab--selected"),
    ]),

    html.Div(id="contenido-rep"),

    html.Div([
        dcc.Link("← Volver al inicio", href="/", className="btn btn-outline-secondary"),
        dcc.Link("Siguiente: Demandas →", href="/demandas",
                 className="btn btn-primary float-end"),
    ], style={"marginTop": "48px", "overflow": "hidden"}),

], className="page-container")


@dash.callback(
    Output("contenido-rep", "children"),
    Input("tabs-rep", "value"),
)
def render_tab(tab):
    if tab == "tab-acciones":
        repertorios = (df.groupby("provincia")[COLS_ACCION].mean() * 100).round(1).T
        repertorios.columns = ["Chubut", "Jujuy"]
        repertorios = repertorios.sort_values("Jujuy")
        long = repertorios.reset_index().melt(id_vars="index")
        fig = px.bar(
            long, x="value", y="index", color="provincia",
            orientation="h", barmode="group",
            color_discrete_map={"Chubut": COLOR_CHUBUT, "Jujuy": COLOR_JUJUY},
            labels={"index": "", "value": "% de eventos", "provincia": ""},
            title="Repertorios por provincia"
        )
        fig.update_layout(height=400)
        fig = aplicar_estilo(fig)
        return html.Div([
            html.H2("Repertorios comparados"),
            html.P("El paro y el corte dominan en Jujuy. Las formas expresivas "
                   "(acto, escrache, destrozos) son exclusivas de Chubut.",
                   className="text-muted"),
            dcc.Graph(figure=fig)
        ])

    elif tab == "tab-actores":
        actores = (df.groupby("provincia")[COLS_ACTORES].mean() * 100).round(1).T
        actores.columns = ["Chubut", "Jujuy"]
        actores = actores.sort_values("Jujuy")
        long = actores.reset_index().melt(id_vars="index")
        fig = px.bar(
            long, x="value", y="index", color="provincia",
            orientation="h", barmode="group",
            color_discrete_map={"Chubut": COLOR_CHUBUT, "Jujuy": COLOR_JUJUY},
            labels={"index": "", "value": "% de eventos", "provincia": ""},
            title="Actores por provincia"
        )
        fig.update_layout(height=500)
        fig = aplicar_estilo(fig)
        return html.Div([
            html.H2("Actores comparados"),
            html.P("Jujuy tiene tres actores con peso masivo (docentes, "
                   "organizaciones sociales, comunidades originarias). "
                   "Chubut tiene un panorama fragmentado: ningún actor supera el 21%.",
                   className="text-muted"),
            dcc.Graph(figure=fig)
        ])

    elif tab == "tab-densidad":
        densidad = df.groupby("provincia")[["n_actores", "n_demandas"]].mean().round(2).reset_index()
        long = densidad.melt(id_vars="provincia")
        fig = px.bar(
            long, x="variable", y="value", color="provincia", barmode="group",
            color_discrete_map={"Chubut": COLOR_CHUBUT, "Jujuy": COLOR_JUJUY},
            labels={"variable": "Métrica", "value": "Promedio por evento", "provincia": ""},
            title="Densidad del evento"
        )
        fig.update_layout(height=400)
        fig = aplicar_estilo(fig)
        return html.Div([
            html.H2("Densidad del evento"),
            html.P("Los eventos de Jujuy promedian 1,77 actores y 1,48 demandas. "
                   "Los de Chubut, 1,01 y 0,95. Los eventos jujeños son "
                   "estructuralmente más densos.",
                   className="text-muted"),
            dcc.Graph(figure=fig)
        ])