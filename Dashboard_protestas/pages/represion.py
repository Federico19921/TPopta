import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

dash.register_page(__name__, path="/represion", name="Represión")

df = pd.read_csv("data/eventos.csv")

COLS_ACCION = ["tiene_marcha", "tiene_corte", "tiene_paro", "tiene_acto",
               "tiene_escrache", "tiene_destrozos", "tiene_toma"]

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

int_prov = pd.crosstab(df["provincia"], df["intervencion_armonizada"],
                       normalize="index").round(3) * 100
int_long = int_prov.T.reset_index().melt(id_vars="intervencion_armonizada")
fig_interv = px.bar(
    int_long, x="intervencion_armonizada", y="value", color="provincia",
    barmode="group",
    color_discrete_map={"Chubut": COLOR_CHUBUT, "Jujuy": COLOR_JUJUY},
    labels={"intervencion_armonizada": "", "value": "% de eventos", "provincia": ""},
    title="Intervención estatal por provincia"
)
fig_interv.update_layout(height=400)
fig_interv = aplicar_estilo(fig_interv)

datos_acc = []
for prov in ["Chubut", "Jujuy"]:
    sub = df[df["provincia"] == prov]
    for accion in COLS_ACCION:
        sub_acc = sub[sub[accion] == 1]
        if len(sub_acc) >= 3:
            n_rep = sub_acc["es_represion"].sum()
            datos_acc.append({
                "provincia": prov,
                "accion": accion.replace("tiene_", ""),
                "%_rep": round(100 * n_rep / len(sub_acc), 1)
            })
df_acc = pd.DataFrame(datos_acc)
fig_acc = px.bar(
    df_acc, x="accion", y="%_rep", color="provincia",
    barmode="group",
    color_discrete_map={"Chubut": COLOR_CHUBUT, "Jujuy": COLOR_JUJUY},
    labels={"accion": "", "%_rep": "% de eventos reprimidos", "provincia": ""},
    title="Represión por tipo de acción"
)
fig_acc.update_layout(height=400)
fig_acc = aplicar_estilo(fig_acc)

tasas = []
for prov in ["Chubut", "Jujuy"]:
    sub = df[df["provincia"] == prov]
    con_datos = sub[sub["intervencion_armonizada"] != "Sin datos"]
    n_rep = sub["es_represion"].sum()
    tasa_bruta = 100 * n_rep / len(sub)
    tasa_ajustada = 100 * n_rep / len(con_datos) if len(con_datos) > 0 else 0
    tasas.append({"provincia": prov, "tipo": "Bruta", "valor": round(tasa_bruta, 1)})
    tasas.append({"provincia": prov, "tipo": "Ajustada", "valor": round(tasa_ajustada, 1)})

df_tasas = pd.DataFrame(tasas)
fig_tasas = px.bar(
    df_tasas, x="provincia", y="valor", color="tipo", barmode="group",
    color_discrete_map={"Bruta": "#B0BEC5", "Ajustada": "#7BB4C2"},
    labels={"provincia": "", "valor": "% de eventos con represión", "tipo": ""},
    title="Tasa de represión: bruta vs ajustada por cobertura"
)
fig_tasas.update_layout(height=400)
fig_tasas = aplicar_estilo(fig_tasas)

df_rep_mes = df[df["es_represion"] == 1].groupby(["mes", "provincia"]).size().reset_index(name="n")
fig_evol = px.bar(
    df_rep_mes, x="mes", y="n", color="provincia", barmode="group",
    color_discrete_map={"Chubut": COLOR_CHUBUT, "Jujuy": COLOR_JUJUY},
    labels={"mes": "Mes", "n": "Eventos con represión", "provincia": ""},
    title="Eventos con represión por mes"
)
fig_evol.update_layout(height=400)
fig_evol = aplicar_estilo(fig_evol)

layout = html.Div([
    html.H1("Represión y respuesta estatal"),
    html.P("El corazón del comparativo: cómo respondió el Estado en cada conflicto.",
           className="text-muted mb-4"),

    html.H2("Intervención estatal"),
    html.P("Jujuy desplegó una intervención más activa que Chubut: "
           "menos ausencia, más monitoreo, más represión y la presencia "
           "exclusiva de disuasión.",
           className="text-muted"),
    dcc.Graph(figure=fig_interv),

    html.H2("Represión por tipo de acción"),
    html.P("El corte es el repertorio más castigado en ambas provincias, "
           "pero mucho más en Jujuy (28,6%) que en Chubut (7,7%).",
           className="text-muted"),
    dcc.Graph(figure=fig_acc),

    html.H2("Tasa ajustada por cobertura"),
    html.P("La tasa bruta está afectada por la diferencia de cobertura entre fuentes. "
           "Al ajustar por eventos con datos, la diferencia se amplía: "
           "Chubut 5,5%, Jujuy 9,4%.",
           className="text-muted"),
    dcc.Graph(figure=fig_tasas),

    html.H2("Evolución temporal de la represión"),
    html.P("En ambos casos la represión se concentra en el mes pico del conflicto.",
           className="text-muted"),
    dcc.Graph(figure=fig_evol),

    html.Div([
        html.H5("Tres hallazgos del bloque de represión"),
        html.Ol([
            html.Li([html.Strong("El corte de ruta es el repertorio más castigado. "),
                     "En Jujuy, el 28,6% de los cortes fueron reprimidos; en Chubut, el 7,7%."]),
            html.Li([html.Strong("La represión en Jujuy fue selectiva. "),
                     "Las comunidades originarias fueron el actor más reprimido (27,8%), "
                     "por encima de los docentes (7,3%)."]),
            html.Li([html.Strong("La disuasión es exclusiva de Jujuy. "),
                     "Es una categoría que no existe en el libro de códigos de Chubut."]),
        ])
    ], className="hallazgo-box"),

    html.Div([
        dcc.Link("← Volver", href="/cruces", className="btn btn-outline-secondary"),
        dcc.Link("Siguiente: Métodos →", href="/metodos",
                 className="btn btn-primary float-end"),
    ], style={"marginTop": "32px", "overflow": "hidden"}),

], className="page-container")