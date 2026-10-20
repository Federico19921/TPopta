import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

dash.register_page(__name__, path="/cruces", name="Cruces")

df = pd.read_csv("data/eventos.csv")

COLS_ACTORES = ["docentes", "gremios_estatales", "sindicatos_privados",
                "organizaciones_sociales", "comunidades_indigenas", "vecinos",
                "colectivos_ambientales", "colectivos_especificos",
                "partidos_politicos", "policias_actores",
                "publico_general", "colectivos_violentos"]

COLS_DEMANDAS = ["demanda_salarial", "demanda_laboral", "demanda_ambiental_territorial",
                 "demanda_politica_legal", "demanda_ddhh", "demanda_servicios",
                 "demanda_derechos_especificos", "demanda_institucional",
                 "demanda_conmemoracion"]

LABELS_ACTORES = {
    "docentes": "Docentes", "gremios_estatales": "Gremios estatales",
    "sindicatos_privados": "Sindicatos privados",
    "organizaciones_sociales": "Org. sociales",
    "comunidades_indigenas": "Comunidades indígenas",
    "vecinos": "Vecinos", "colectivos_ambientales": "Colectivos ambientales",
    "colectivos_especificos": "Colectivos específicos",
    "partidos_politicos": "Partidos políticos",
    "policias_actores": "Policías (actores)",
    "publico_general": "Público general",
    "colectivos_violentos": "Colectivos violentos",
}

LABELS_DEMANDAS = {
    "demanda_salarial": "Salarial", "demanda_laboral": "Laboral",
    "demanda_ambiental_territorial": "Ambiental-territorial",
    "demanda_politica_legal": "Política-legal", "demanda_ddhh": "DDHH",
    "demanda_servicios": "Servicios",
    "demanda_derechos_especificos": "Derechos específicos",
    "demanda_institucional": "Institucional",
    "demanda_conmemoracion": "Conmemoración",
}

def aplicar_estilo(fig):
    fig.update_layout(
        font=dict(family="Inter, sans-serif", size=12, color="#374151"),
        title=dict(font=dict(size=14, color="#151515"), x=0, xanchor="left"),
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=40, r=20, t=50, b=40),
        hoverlabel=dict(bgcolor="white")
    )
    return fig

layout = html.Div([
    html.H1("Cruces: actores, demandas y represión"),
    html.P("Análisis de las relaciones entre quién protesta, qué reclama y quién es reprimido.",
           className="text-muted mb-4"),

    html.Div([
        dbc.Row([
            dbc.Col([
                html.Label("Provincia", className="kpi-label"),
                dcc.Dropdown(
                    id="cruces-provincia",
                    options=[{"label": "Todas", "value": "Todas"}] +
                            [{"label": p, "value": p} for p in df["provincia"].unique()],
                    value="Todas",
                    clearable=False
                )
            ], width=6),
            dbc.Col([
                html.Label("Solo eventos con represión", className="kpi-label"),
                dcc.Checklist(
                    id="cruces-solo-represion",
                    options=[{"label": "Sí", "value": "si"}],
                    value=[]
                )
            ], width=6),
        ])
    ], className="mb-4"),

    html.H2("Actor × Demanda"),
    html.P("Qué reclama cada actor. Los valores son la cantidad de eventos "
           "donde coexisten ambos.",
           className="text-muted"),
    dcc.Graph(id="cruces-matriz-actor-demanda"),

    html.H2("Actor × Represión"),
    html.P("Qué actor fue reprimido proporcionalmente.",
           className="text-muted"),
    dcc.Graph(id="cruces-actor-represion"),

    html.H2("Demanda × Represión"),
    html.P("Qué demanda fue reprimida proporcionalmente.",
           className="text-muted"),
    dcc.Graph(id="cruces-demanda-represion"),

    html.H2("Eventos con represión (detalle)"),
    html.P("Listado completo de los eventos que tuvieron algún tipo "
           "de intervención represiva.",
           className="text-muted"),
    html.Div(id="cruces-tabla-represion"),

    html.Div([
        html.H5("Lecturas de los cruces"),
        html.Ul([
            html.Li("El corte es la acción más castigada, pero solo cuando "
                    "va acompañado de comunidades indígenas u organizaciones sociales."),
            html.Li("En Jujuy, la demanda política-legal es la más reprimida "
                    "(5 de 39 eventos); en Chubut, la ambiental-territorial (3 de 40)."),
            html.Li("Los actores con menos recursos institucionales son los más "
                    "castigados proporcionalmente."),
        ])
    ], className="hallazgo-box"),

    html.Div([
        dcc.Link("← Volver", href="/demandas", className="btn btn-outline-secondary"),
        dcc.Link("Siguiente: Represión →", href="/represion",
                 className="btn btn-primary float-end"),
    ], style={"marginTop": "32px", "overflow": "hidden"}),

], className="page-container")


@dash.callback(
    Output("cruces-matriz-actor-demanda", "figure"),
    Output("cruces-actor-represion", "figure"),
    Output("cruces-demanda-represion", "figure"),
    Output("cruces-tabla-represion", "children"),
    Input("cruces-provincia", "value"),
    Input("cruces-solo-represion", "value"),
)
def actualizar(provincia, solo_rep):
    dff = df.copy()
    if provincia != "Todas":
        dff = dff[dff["provincia"] == provincia]
    if "si" in solo_rep:
        dff = dff[dff["es_represion"] == 1]

    matriz = pd.DataFrame(0, index=list(LABELS_ACTORES.values()),
                          columns=list(LABELS_DEMANDAS.values()))
    for _, row in dff.iterrows():
        actores_presentes = [LABELS_ACTORES[a] for a in COLS_ACTORES if row[a] == 1]
        demandas_presentes = [LABELS_DEMANDAS[d] for d in COLS_DEMANDAS if row[d] == 1]
        for a in actores_presentes:
            for d in demandas_presentes:
                matriz.loc[a, d] += 1

    matriz = matriz.loc[matriz.sum(axis=1) > 0, matriz.sum(axis=0) > 0]

    if matriz.empty:
        fig_matriz = px.bar(title="Sin datos para el filtro actual")
    else:
        fig_matriz = go.Figure(data=go.Heatmap(
            z=matriz.values,
            x=matriz.columns.tolist(),
            y=matriz.index.tolist(),
            colorscale="Blues",
            text=matriz.values,
            texttemplate="%{text}",
            textfont={"size": 10},
            hovertemplate="Actor: %{y}<br>Demanda: %{x}<br>Eventos: %{z}<extra></extra>"
        ))
        fig_matriz.update_layout(
            height=500,
            xaxis_tickangle=-45,
            margin=dict(l=180, r=20, t=20, b=120)
        )
        fig_matriz = aplicar_estilo(fig_matriz)

    datos_actor = []
    for actor in COLS_ACTORES:
        sub_act = dff[dff[actor] == 1]
        if len(sub_act) >= 3:
            n_rep = sub_act["es_represion"].sum()
            datos_actor.append({
                "actor": LABELS_ACTORES[actor],
                "n": len(sub_act),
                "n_rep": n_rep,
                "%_rep": round(100 * n_rep / len(sub_act), 1)
            })

    if datos_actor:
        df_actor = pd.DataFrame(datos_actor).sort_values("%_rep")
        fig_actor = px.bar(
            df_actor, x="%_rep", y="actor", orientation="h",
            color="%_rep", color_continuous_scale="Reds",
            labels={"%_rep": "% de eventos reprimidos", "actor": ""},
            title="Represión por actor"
        )
        fig_actor.update_layout(height=400, coloraxis_showscale=False)
        fig_actor = aplicar_estilo(fig_actor)
    else:
        fig_actor = px.bar(title="Sin datos suficientes")

    datos_dem = []
    for dem in COLS_DEMANDAS:
        sub_dem = dff[dff[dem] == 1]
        if len(sub_dem) >= 3:
            n_rep = sub_dem["es_represion"].sum()
            datos_dem.append({
                "demanda": LABELS_DEMANDAS[dem],
                "n": len(sub_dem),
                "n_rep": n_rep,
                "%_rep": round(100 * n_rep / len(sub_dem), 1)
            })

    if datos_dem:
        df_dem = pd.DataFrame(datos_dem).sort_values("%_rep")
        fig_dem = px.bar(
            df_dem, x="%_rep", y="demanda", orientation="h",
            color="%_rep", color_continuous_scale="Oranges",
            labels={"%_rep": "% de eventos reprimidos", "demanda": ""},
            title="Represión por demanda"
        )
        fig_dem.update_layout(height=400, coloraxis_showscale=False)
        fig_dem = aplicar_estilo(fig_dem)
    else:
        fig_dem = px.bar(title="Sin datos suficientes")

    rep_df = dff[dff["es_represion"] == 1].copy()
    if len(rep_df) > 0:
        rep_df["actores"] = rep_df.apply(
            lambda r: ", ".join([LABELS_ACTORES[a] for a in COLS_ACTORES if r[a] == 1]),
            axis=1
        )
        rep_df["demandas"] = rep_df.apply(
            lambda r: ", ".join([LABELS_DEMANDAS[d] for d in COLS_DEMANDAS if r[d] == 1]),
            axis=1
        )
        tabla = rep_df[["fecha", "provincia", "localidad", "tipo_accion",
                        "actores", "demandas"]].copy()
        tabla.columns = ["Fecha", "Provincia", "Localidad", "Acción",
                         "Actores", "Demandas"]
        tabla = tabla.sort_values(["Provincia", "Fecha"])
        tabla_html = dbc.Table.from_dataframe(
            tabla, striped=True, bordered=False, hover=True, size="sm"
        )
    else:
        tabla_html = html.P("No hay eventos con represión en el filtro actual.",
                            className="text-muted")

    return fig_matriz, fig_actor, fig_dem, tabla_html