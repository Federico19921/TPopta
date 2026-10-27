import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
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
        plot_bgcolor="white", paper_bgcolor="white",
        margin=dict(l=0, r=0, t=20, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0, title=None),
        xaxis=dict(showgrid=False, showline=False, zeroline=False),
        yaxis=dict(showgrid=True, gridcolor="#F3F4F6", showline=False, zeroline=False)
    )
    return fig

def chart_box(titulo, subtitulo, fig):
    return html.Div([
        html.Div([html.P(titulo, className="chart-title")], className="chart-header"),
        html.P(subtitulo, className="chart-subtitle"),
        html.Div(dcc.Graph(figure=fig, config={'displayModeBar': False}), className="chart-body"),
        html.Div("Fuente: Base propia de eventos.", className="chart-footer")
    ], className="chart-container")

def construir_matriz(sub):
    matriz = pd.DataFrame(0, index=list(LABELS_ACTORES.values()), columns=list(LABELS_DEMANDAS.values()))
    for _, row in sub.iterrows():
        actores = [LABELS_ACTORES[a] for a in COLS_ACTORES if row[a] == 1]
        demandas = [LABELS_DEMANDAS[d] for d in COLS_DEMANDAS if row[d] == 1]
        for a in actores:
            for d in demandas:
                matriz.loc[a, d] += 1
    return matriz.loc[matriz.sum(axis=1) > 0, matriz.sum(axis=0) > 0]

layout = html.Div([
    html.Div("Inicio | Trabajo e ingresos | Cruces", className="breadcrumbs"),
    html.Div([
        html.H1("Cruces: actores, demandas y represión"),
        html.P("Análisis de las relaciones entre quién protesta, qué reclama y quién es reprimido.", style={"fontSize": "1.1rem", "color": "#4B5563"}),

        html.Div([
            html.H4("Mensajes clave", className="mensajes-clave-title"),
            dbc.Row([
                dbc.Col(html.Div("En Jujuy, la demanda política-legal es la más reprimida (5 de 39 eventos).", className="mensaje-card destacado"), width=6),
                dbc.Col(html.Div("Los actores con menos recursos institucionales son los más castigados proporcionalmente.", className="mensaje-card"), width=6),
            ])
        ], className="mensajes-clave-wrapper"),

        html.Div([
            dbc.Checklist(id="cruces-solo-represion", options=[{"label": "Mostrar solo eventos con represión", "value": "si"}], value=[], switch=True)
        ], style={"marginBottom": "24px", "fontWeight": "bold"}),

        html.Div(id="contenedor-cruces"),

        html.Div([
            dcc.Link("← Volver", href="/demandas", className="btn btn-outline-secondary"),
            dcc.Link("Siguiente: Represión →", href="/represion", className="btn btn-primary float-end"),
        ], style={"marginTop": "40px", "overflow": "hidden"}),
    ], className="page-container")
])

@dash.callback(
    Output("contenedor-cruces", "children"),
    Input("cruces-solo-represion", "value")
)
def actualizar(solo_rep):
    dff = df.copy()
    if "si" in solo_rep:
        dff = dff[dff["es_represion"] == 1]

    ch = construir_matriz(dff[dff["provincia"] == "Chubut"])
    ju = construir_matriz(dff[dff["provincia"] == "Jujuy"])
    todas_act = sorted(set(ch.index) | set(ju.index))
    todas_dem = sorted(set(ch.columns) | set(ju.columns))
    ch = ch.reindex(index=todas_act, columns=todas_dem, fill_value=0)
    ju = ju.reindex(index=todas_act, columns=todas_dem, fill_value=0)

    if todas_act and todas_dem:
        fig_matriz = make_subplots(rows=1, cols=2, subplot_titles=("Chubut", "Jujuy"), shared_yaxes=True, horizontal_spacing=0.08)
        fig_matriz.add_trace(go.Heatmap(z=ch.values, x=todas_dem, y=todas_act, colorscale="Blues", showscale=False,
                                        text=ch.values, texttemplate="%{text}", textfont={"size": 9}), row=1, col=1)
        fig_matriz.add_trace(go.Heatmap(z=ju.values, x=todas_dem, y=todas_act, colorscale="Reds", showscale=False,
                                        text=ju.values, texttemplate="%{text}", textfont={"size": 9}), row=1, col=2)
        fig_matriz.update_layout(height=550, margin=dict(l=160, r=20, t=60, b=140))
        fig_matriz.update_xaxes(tickangle=-45)
        fig_matriz = aplicar_estilo(fig_matriz)
    else:
        fig_matriz = px.bar(title="Sin datos")

    datos_actor = []
    for prov in ["Chubut", "Jujuy"]:
        sub_p = dff[dff["provincia"] == prov]
        for actor in COLS_ACTORES:
            sub_a = sub_p[sub_p[actor] == 1]
            if len(sub_a) >= 3:
                n_rep = sub_a["es_represion"].sum()
                datos_actor.append({"provincia": prov, "actor": LABELS_ACTORES[actor], "n": len(sub_a), "%_rep": round(100 * n_rep / len(sub_a), 1)})
    
    fig_actor = px.bar(pd.DataFrame(datos_actor).sort_values("%_rep"), x="%_rep", y="actor", color="provincia", orientation="h", barmode="group",
                       color_discrete_map={"Chubut": "#2E86AB", "Jujuy": "#A23B72"}, labels={"%_rep": "% eventos reprimidos", "actor": "", "provincia": ""}) if datos_actor else px.bar(title="Sin datos")
    fig_actor.update_layout(height=400)
    fig_actor = aplicar_estilo(fig_actor)

    datos_dem = []
    for prov in ["Chubut", "Jujuy"]:
        sub_p = dff[dff["provincia"] == prov]
        for dem in COLS_DEMANDAS:
            sub_d = sub_p[sub_p[dem] == 1]
            if len(sub_d) >= 3:
                n_rep = sub_d["es_represion"].sum()
                datos_dem.append({"provincia": prov, "demanda": LABELS_DEMANDAS[dem], "n": len(sub_d), "%_rep": round(100 * n_rep / len(sub_d), 1)})
    
    fig_dem = px.bar(pd.DataFrame(datos_dem).sort_values("%_rep"), x="%_rep", y="demanda", color="provincia", orientation="h", barmode="group",
                     color_discrete_map={"Chubut": "#2E86AB", "Jujuy": "#A23B72"}, labels={"%_rep": "% eventos reprimidos", "demanda": "", "provincia": ""}) if datos_dem else px.bar(title="Sin datos")
    fig_dem.update_layout(height=400)
    fig_dem = aplicar_estilo(fig_dem)

    return html.Div([
        chart_box("Matriz Actor × Demanda", "Cantidad de eventos donde coexisten ambos.", fig_matriz),
        chart_box("Represión por actor", "Porcentaje de eventos de cada actor que sufrieron represión.", fig_actor),
        chart_box("Represión por demanda", "Porcentaje de eventos de cada demanda que sufrieron represión.", fig_dem)
    ])