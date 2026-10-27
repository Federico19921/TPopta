import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

dash.register_page(__name__, path="/represion", name="Represión")

df = pd.read_csv("data/eventos.csv")

COLS_ACCION = ["tiene_marcha", "tiene_corte", "tiene_paro", "tiene_acto", "tiene_escrache", "tiene_destrozos", "tiene_toma"]
COLOR_CHUBUT = "#2E86AB"
COLOR_JUJUY = "#A23B72"

def aplicar_estilo(fig):
    fig.update_layout(
        font=dict(family="Arial, sans-serif", size=12, color="#4B5563"),
        plot_bgcolor="white", paper_bgcolor="white", margin=dict(l=0, r=0, t=10, b=40),
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

int_prov = pd.crosstab(df["provincia"], df["intervencion_armonizada"], normalize="index").round(3) * 100
int_long = int_prov.T.reset_index().melt(id_vars="intervencion_armonizada")
fig_interv = px.bar(int_long, x="intervencion_armonizada", y="value", color="provincia", barmode="group",
                    color_discrete_map={"Chubut": COLOR_CHUBUT, "Jujuy": COLOR_JUJUY},
                    labels={"intervencion_armonizada": "", "value": "% de eventos", "provincia": ""})
fig_interv.update_layout(height=350)
fig_interv = aplicar_estilo(fig_interv)

datos_acc = []
for prov in ["Chubut", "Jujuy"]:
    sub = df[df["provincia"] == prov]
    for accion in COLS_ACCION:
        sub_acc = sub[sub[accion] == 1]
        if len(sub_acc) >= 3:
            n_rep = sub_acc["es_represion"].sum()
            datos_acc.append({"provincia": prov, "accion": accion.replace("tiene_", ""), "%_rep": round(100 * n_rep / len(sub_acc), 1)})
fig_acc = px.bar(pd.DataFrame(datos_acc), x="accion", y="%_rep", color="provincia", barmode="group",
                 color_discrete_map={"Chubut": COLOR_CHUBUT, "Jujuy": COLOR_JUJUY},
                 labels={"accion": "", "%_rep": "% de eventos reprimidos", "provincia": ""})
fig_acc.update_layout(height=350)
fig_acc = aplicar_estilo(fig_acc)

tasas = []
for prov in ["Chubut", "Jujuy"]:
    sub = df[df["provincia"] == prov]
    con_datos = sub[sub["intervencion_armonizada"] != "Sin datos"]
    n_rep = sub["es_represion"].sum()
    tasas.append({"provincia": prov, "tipo": "Bruta", "valor": round(100 * n_rep / len(sub), 1)})
    tasas.append({"provincia": prov, "tipo": "Ajustada", "valor": round(100 * n_rep / len(con_datos), 1)})
fig_tasas = px.bar(pd.DataFrame(tasas), x="provincia", y="valor", color="tipo", barmode="group",
                   color_discrete_map={"Bruta": "#B0BEC5", "Ajustada": "#7BB4C2"},
                   labels={"provincia": "", "valor": "% eventos con represión", "tipo": ""})
fig_tasas.update_layout(height=350)
fig_tasas = aplicar_estilo(fig_tasas)

df_rep_mes = df[df["es_represion"] == 1].groupby(["mes", "provincia"]).size().reset_index(name="n")
fig_evol = px.bar(df_rep_mes, x="mes", y="n", color="provincia", barmode="group",
                  color_discrete_map={"Chubut": COLOR_CHUBUT, "Jujuy": COLOR_JUJUY},
                  labels={"mes": "Mes", "n": "Eventos con represión", "provincia": ""})
fig_evol.update_layout(height=350)
fig_evol = aplicar_estilo(fig_evol)

layout = html.Div([
    html.Div("Inicio | Trabajo e ingresos | Represión", className="breadcrumbs"),
    html.Div([
        html.H1("Represión y respuesta estatal"),
        html.P("Análisis de cómo respondió el Estado en cada conflicto y cuál fue el blanco de la represión.", style={"fontSize": "1.1rem", "color": "#4B5563"}),

        html.Div([
            html.H4("Mensajes clave", className="mensajes-clave-title"),
            dbc.Row([
                dbc.Col(html.Div("Jujuy tuvo más represión (7,6%) y disuasión exclusiva (3,0%).", className="mensaje-card"), width=4),
                dbc.Col(html.Div("El corte de ruta fue el repertorio más castigado: 28,6% en Jujuy vs 7,7% en Chubut.", className="mensaje-card destacado"), width=4),
                dbc.Col(html.Div("Las comunidades originarias fueron el actor más reprimido en Jujuy (27,8%).", className="mensaje-card"), width=4),
            ])
        ], className="mensajes-clave-wrapper"),

        chart_box("Intervención estatal", "Distribución de los tipos de intervención del Estado en cada provincia.", fig_interv),
        chart_box("Represión por tipo de acción", "Porcentaje de eventos de cada repertorio que sufrieron represión.", fig_acc),
        chart_box("Tasa ajustada por cobertura", "Comparación de la tasa bruta vs la tasa calculada solo con eventos con datos.", fig_tasas),
        chart_box("Evolución temporal de la represión", "Cantidad de eventos con represión por mes.", fig_evol),

        html.Div([
            dcc.Link("← Volver", href="/cruces", className="btn btn-outline-secondary"),
            dcc.Link("Siguiente: Métodos →", href="/metodos", className="btn btn-primary float-end"),
        ], style={"marginTop": "40px", "overflow": "hidden"}),
    ], className="page-container")
])