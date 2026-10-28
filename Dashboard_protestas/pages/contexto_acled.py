import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

dash.register_page(__name__, path="/acled", name="Contexto ACLED")

# --- DATOS SIMULADOS (reemplazar por tus datos reales de ACLED) ---
# Cuando tengas el CSV de ACLED nacional, hacés:
# acled = pd.read_csv("data/acled_argentina.csv")
# Y adaptás los groupby.

# Por ahora, datos exactos de tu notebook de ACLED 2020-2024
por_anio = pd.DataFrame({
    "anio": [2020, 2021, 2022, 2023, 2024],
    "protestas": [2818, 2864, 2513, 2447, 1832],
    "represion": [94, 100, 62, 62, 46]
})

top_provincias = pd.DataFrame({
    "provincia": ["Buenos Aires", "CABA", "Tucumán", "Santa Fe", "Córdoba", "Jujuy", "Chubut", "Formosa", "Santa Cruz", "Chaco"],
    "represion": [68, 62, 30, 26, 24, 18, 18, 16, 14, 14]
})

tasas_comparadas = pd.DataFrame({
    "ambito": ["Nacional", "Chubut", "Jujuy"],
    "tasa": [2.92, 1.11, 6.12],
    "tipo": ["Nacional", "Provincia", "Provincia"]
})

# --- ESTILOS ---
COLOR_CHUBUT = "#2E86AB"
COLOR_JUJUY = "#A23B72"
COLOR_NACIONAL = "#6B7280"

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
        html.Div("Fuente: ACLED (Armed Conflict Location & Event Data Project), 2020-2024.", className="chart-footer")
    ], className="chart-container")

# --- GRÁFICO 1: Evolución anual nacional ---
fig_anual = go.Figure()
fig_anual.add_trace(go.Bar(x=por_anio["anio"], y=por_anio["protestas"], name="Protestas", marker_color="#7BB4C2"))
fig_anual.add_trace(go.Bar(x=por_anio["anio"], y=por_anio["represion"], name="Represión", marker_color="#E53935"))
fig_anual.update_layout(barmode="group", height=350)
fig_anual = aplicar_estilo(fig_anual)

# --- GRÁFICO 2: Top 10 provincias por represión ---
top_provincias["destacar"] = top_provincias["provincia"].isin(["Chubut", "Jujuy"])
fig_ranking = px.bar(
    top_provincias.sort_values("represion"),
    x="represion", y="provincia", orientation="h",
    color="destacar",
    color_discrete_map={True: "#E53935", False: "#B0BEC5"},
    labels={"represion": "Eventos de represión", "provincia": ""}
)
fig_ranking.update_layout(showlegend=False, height=400)
fig_ranking = aplicar_estilo(fig_ranking)

# --- GRÁFICO 3: Tasas comparadas ---
fig_tasas = px.bar(
    tasas_comparadas, x="ambito", y="tasa", color="ambito",
    color_discrete_map={"Nacional": COLOR_NACIONAL, "Chubut": COLOR_CHUBUT, "Jujuy": COLOR_JUJUY},
    labels={"ambito": "", "tasa": "% de eventos con represión"}
)
fig_tasas.update_layout(showlegend=False, height=350)
fig_tasas = aplicar_estilo(fig_tasas)

# --- LAYOUT ---
layout = html.Div([
    html.Div("Inicio | Trabajo e ingresos | Contexto Nacional", className="breadcrumbs"),
    html.Div([
        html.H1("Contexto nacional de la protesta"),
        html.P("Para dimensionar los casos de Chubut y Jujuy, se consultó la base ACLED para todo el país en el período 2020-2024.", style={"fontSize": "1.1rem", "color": "#4B5563"}),

        html.Div([
            html.H4("Mensajes clave", className="mensajes-clave-title"),
            dbc.Row([
                dbc.Col(html.Div("Argentina registró 12.474 protestas entre 2020 y 2024.", className="mensaje-card"), width=4),
                dbc.Col(html.Div("Solo el 2,92% de esos eventos involucraron represión estatal.", className="mensaje-card"), width=4),
                dbc.Col(html.Div("Jujuy tuvo una tasa de represión del 6,12% (más del doble del promedio), mientras que Chubut registró 1,11% (muy por debajo).", className="mensaje-card destacado"), width=4),
            ])
        ], className="mensajes-clave-wrapper"),

        chart_box("Evolución anual de protestas y represión", "Cantidad de eventos en Argentina (2020-2024).", fig_anual),
        chart_box("Ranking de provincias por represión", "Top 10 provincias. En rojo, los casos de Chubut y Jujuy.", fig_ranking),
        chart_box("Tasas de represión comparadas", "Porcentaje de eventos con represión sobre el total de protestas.", fig_tasas),

        html.Div([
            html.H5("Por qué ACLED sirve como contexto, pero no como fuente principal"),
            html.P("ACLED es una base global que prioriza eventos violentos con víctimas fatales. Para protestas pacíficas o de baja intensidad, su cobertura es estructuralmente menor que la de fuentes locales. En los períodos analizados, ACLED solo registró 8 eventos de represión para Chubut y Jujuy combinadas. Por eso se usó la base propia como fuente principal, y ACLED solo para mostrar el contexto nacional.")
        ], className="hallazgo-box"),

        html.Div([
            dcc.Link("← Volver", href="/represion", className="btn btn-outline-secondary"),
            dcc.Link("Siguiente: Métodos →", href="/metodos", className="btn btn-primary float-end"),
        ], style={"marginTop": "40px", "overflow": "hidden"}),
    ], className="page-container")
])