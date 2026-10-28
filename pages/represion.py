import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

dash.register_page(__name__, path="/represion", name="Represión")

df = pd.read_csv("data/eventos.csv")

COLS_ACCION = ["tiene_marcha", "tiene_corte", "tiene_paro", "tiene_acto", "tiene_escrache", "tiene_destrozos", "tiene_toma"]
COLS_ACTORES = ["docentes", "gremios_estatales", "sindicatos_privados", "organizaciones_sociales", "comunidades_indigenas", "vecinos", "colectivos_ambientales", "colectivos_especificos", "partidos_politicos", "policias_actores", "publico_general", "colectivos_violentos"]
COLS_DEMANDAS = ["demanda_salarial", "demanda_laboral", "demanda_ambiental_territorial", "demanda_politica_legal", "demanda_ddhh", "demanda_servicios", "demanda_derechos_especificos", "demanda_institucional", "demanda_conmemoracion"]

LABELS_ACTORES = {"docentes": "Docentes", "gremios_estatales": "Gremios estatales", "sindicatos_privados": "Sindicatos privados", "organizaciones_sociales": "Org. sociales", "comunidades_indigenas": "Comunidades indígenas", "vecinos": "Vecinos", "colectivos_ambientales": "Colectivos ambientales", "colectivos_especificos": "Colectivos específicos", "partidos_politicos": "Partidos políticos", "policias_actores": "Policías", "publico_general": "Público general", "colectivos_violentos": "Colectivos violentos"}
LABELS_DEMANDAS = {"demanda_salarial": "Salarial", "demanda_laboral": "Laboral", "demanda_ambiental_territorial": "Ambiental", "demanda_politica_legal": "Política", "demanda_ddhh": "DDHH", "demanda_servicios": "Servicios", "demanda_derechos_especificos": "Dchos. específicos", "demanda_institucional": "Institucional", "demanda_conmemoracion": "Conmemoración"}

COLOR_CHUBUT = "#2E86AB"
COLOR_JUJUY = "#A23B72"

def aplicar_estilo(fig):
    fig.update_layout(
        font=dict(family="Arial, sans-serif", size=12, color="#4B5563"),
        plot_bgcolor="white", 
        paper_bgcolor="white", 
        margin=dict(l=0, r=0, t=10, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0, title=None),
        xaxis=dict(showgrid=False, showline=False, zeroline=False),
        yaxis=dict(showgrid=True, gridcolor="#F3F4F6", showline=False, zeroline=False),
        
        # --- LAS MAGIAS PARA QUE NO QUEDEN TOSCAS ---
        bargap=0.3,       # Espacio entre grupos de barras (ej: entre 2020 y 2021)
        bargroupgap=0.1   # Espacio entre barras del mismo grupo (ej: Chubut vs Jujuy)
    )
    
    # Achica el grosor de la barra en sí (por defecto es 1.0 o automático)
    fig.update_traces(width=0.4) 
    
    return fig

def chart_box(titulo, subtitulo, fig):
    return html.Div([
        html.Div([html.P(titulo, className="chart-title")], className="chart-header"),
        html.P(subtitulo, className="chart-subtitle"),
        html.Div(dcc.Graph(figure=fig, config={'displayModeBar': False}), className="chart-body"),
        html.Div("Fuente: Base propia de eventos.", className="chart-footer")
    ], className="chart-container")

# 1. Intervención estatal
int_prov = pd.crosstab(df["provincia"], df["intervencion_armonizada"], normalize="index").round(3) * 100
int_long = int_prov.T.reset_index().melt(id_vars="intervencion_armonizada")
fig_interv = px.bar(int_long, x="intervencion_armonizada", y="value", color="provincia", barmode="group",
                    color_discrete_map={"Chubut": COLOR_CHUBUT, "Jujuy": COLOR_JUJUY},
                    labels={"intervencion_armonizada": "", "value": "% de eventos", "provincia": ""})
fig_interv.update_layout(height=350)
fig_interv = aplicar_estilo(fig_interv)

# 2. Represión por tipo de acción
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

# 3. Represión por actor
datos_actor = []
for prov in ["Chubut", "Jujuy"]:
    sub_p = df[df["provincia"] == prov]
    for actor in COLS_ACTORES:
        sub_a = sub_p[sub_p[actor] == 1]
        if len(sub_a) >= 3:
            n_rep = sub_a["es_represion"].sum()
            datos_actor.append({"provincia": prov, "actor": LABELS_ACTORES[actor], "%_rep": round(100 * n_rep / len(sub_a), 1)})
fig_actor = px.bar(pd.DataFrame(datos_actor).sort_values("%_rep"), x="%_rep", y="actor", color="provincia", orientation="h", barmode="group",
                   color_discrete_map={"Chubut": COLOR_CHUBUT, "Jujuy": COLOR_JUJUY}, labels={"%_rep": "% eventos reprimidos", "actor": "", "provincia": ""})
fig_actor.update_layout(height=400)
fig_actor = aplicar_estilo(fig_actor)

# 4. Represión por demanda
datos_dem = []
for prov in ["Chubut", "Jujuy"]:
    sub_p = df[df["provincia"] == prov]
    for dem in COLS_DEMANDAS:
        sub_d = sub_p[sub_p[dem] == 1]
        if len(sub_d) >= 3:
            n_rep = sub_d["es_represion"].sum()
            datos_dem.append({"provincia": prov, "demanda": LABELS_DEMANDAS[dem], "%_rep": round(100 * n_rep / len(sub_d), 1)})
fig_dem = px.bar(pd.DataFrame(datos_dem).sort_values("%_rep"), x="%_rep", y="demanda", color="provincia", orientation="h", barmode="group",
                 color_discrete_map={"Chubut": COLOR_CHUBUT, "Jujuy": COLOR_JUJUY}, labels={"%_rep": "% eventos reprimidos", "demanda": "", "provincia": ""})
fig_dem.update_layout(height=350)
fig_dem = aplicar_estilo(fig_dem)

# 5. Tasa ajustada por cobertura
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

# 6. Judicialización (Tasa y Repertorios)
df_jud = df[df["judicializacion"] != 99].copy()
df_jud["judicializado"] = (df_jud["judicializacion"] == 1).astype(int)
tasa_jud_data = []
for prov in ["Chubut", "Jujuy"]:
    sub = df_jud[df_jud["provincia"] == prov]
    if len(sub) > 0:
        tasa_jud_data.append({"provincia": prov, "tasa": round(100 * sub["judicializado"].sum() / len(sub), 1)})
fig_jud_tasa = px.bar(pd.DataFrame(tasa_jud_data), x="provincia", y="tasa", color="provincia",
                      color_discrete_map={"Chubut": COLOR_CHUBUT, "Jujuy": COLOR_JUJUY}, labels={"provincia": "", "tasa": "% eventos judicializados"})
fig_jud_tasa.update_layout(height=350, showlegend=False)
fig_jud_tasa = aplicar_estilo(fig_jud_tasa)

df_jud_1 = df[df["judicializacion"] == 1]
if len(df_jud_1) > 0:
    jud_acc = df_jud_1["tipo_accion"].value_counts().reset_index()
    jud_acc.columns = ["accion", "cantidad"]
    fig_jud_acc = px.bar(jud_acc, x="cantidad", y="accion", orientation="h", color="accion",
                         color_discrete_sequence=["#7BB4C2"], labels={"accion": "", "cantidad": "Eventos judicializados"})
    fig_jud_acc.update_layout(height=350, showlegend=False)
    fig_jud_acc = aplicar_estilo(fig_jud_acc)
else:
    fig_jud_acc = px.bar(title="Sin datos")

# --- LAYOUT ---
layout = html.Div([
    html.Div("Inicio | Trabajo e ingresos | Represión", className="breadcrumbs"),
    html.Div([
        html.H1("Represión y respuesta estatal"),
        html.P("Análisis de cómo respondió el Estado en cada conflicto, a quién castigó y qué herramientas usó.", style={"fontSize": "1.1rem", "color": "#4B5563"}),

        html.Div([
            html.H4("Mensajes clave", className="mensajes-clave-title"),
            dbc.Row([
                dbc.Col(html.Div("Jujuy tuvo más represión (7,6%) y disuasión exclusiva (3,0%).", className="mensaje-card"), width=3),
                dbc.Col(html.Div("El corte de ruta fue el repertorio más castigado: 28,6% en Jujuy vs 7,7% en Chubut.", className="mensaje-card destacado"), width=3),
                dbc.Col(html.Div("Las comunidades originarias fueron el actor más reprimido en Jujuy (27,8%).", className="mensaje-card"), width=3),
                dbc.Col(html.Div("En Jujuy, el 100% de las causas judiciales fueron por cortes de ruta.", className="mensaje-card"), width=3),
            ])
        ], className="mensajes-clave-wrapper"),

        chart_box("Intervención estatal", "Distribución de los tipos de intervención del Estado en cada provincia.", fig_interv),
        chart_box("Represión por tipo de acción", "Porcentaje de eventos de cada repertorio que sufrieron represión.", fig_acc),
        
        html.H2("¿A quién se reprimió?"),
        chart_box("Represión por actor", "Porcentaje de eventos de cada actor que sufrieron represión.", fig_actor),
        chart_box("Represión por demanda", "Porcentaje de eventos de cada demanda que sufrieron represión.", fig_dem),

        html.H2("El uso de la justicia"),
        chart_box("Tasa de judicialización", "Porcentaje de eventos con causas judiciales sobre el total de eventos con datos.", fig_jud_tasa),
        chart_box("Repertorios judicializados", "Tipos de acción que terminaron en causas judiciales.", fig_jud_acc),

        html.Div([
            html.H5("La represión como estrategia selectiva"),
            html.P("En Jujuy, la represión no fue indiscriminada: se dirigió con mayor intensidad hacia comunidades originarias (27,8%) que hacia docentes (7,3%), a pesar de que los docentes fueron el actor más movilizado. Además, la justicia se usó como herramienta de disciplinamiento: el 71,4% de los eventos con datos terminaron en causas judiciales, y el 100% de ellas fueron por cortes de ruta. En Chubut, en cambio, las 7 causas judiciales se distribuyeron entre manifestaciones, marchas, destrozos y cortes, mostrando una respuesta legal más reactiva y menos focalizada.")
        ], className="hallazgo-box"),

        html.Div([
            dcc.Link("← Volver", href="/cruces", className="btn btn-outline-secondary"),
            dcc.Link("Siguiente: Contexto ACLED →", href="/acled", className="btn btn-primary float-end"),
        ], style={"marginTop": "40px", "overflow": "hidden"}),
    ], className="page-container")
])