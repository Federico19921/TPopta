import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

dash.register_page(__name__, path="/panorama", name="Panorama")

df = pd.read_csv("data/eventos.csv")
df["fecha"] = pd.to_datetime(df["fecha"])

COLOR_CHUBUT = "#2E86AB"
COLOR_JUJUY = "#A23B72"

# Configuración de Plotly limpia (sin cuadros)
def aplicar_estilo(fig):
    fig.update_layout(
        font=dict(family="Arial, sans-serif", size=12, color="#4B5563"),
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=0, r=0, t=10, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.02,
                    xanchor="left", x=0, title=None),
        xaxis=dict(showgrid=False, showline=False, zeroline=False),
        yaxis=dict(showgrid=True, gridcolor="#F3F4F6",
                   showline=False, zeroline=False),
        # estas dos solo afectan a bar, son inocuas si no hay barras
        bargap=0.3,
        bargroupgap=0.1,
    )

    # Aplicar props específicas según el tipo de trace
    for tr in fig.data:
        if tr.type == "bar":
            tr.update(width=0.4)
        elif tr.type == "scatter":
            # si querés controlar la línea/markers:
            tr.update(line=dict(width=2), marker=dict(size=7))
        elif tr.type == "heatmap":
            tr.update(xgap=2, ygap=2)

    return fig

df["mes"] = df["fecha"].dt.to_period("M").astype(str)
serie = df.groupby(["mes", "provincia"]).size().reset_index(name="n")

fig_serie = px.line(
    serie, x="mes", y="n", color="provincia", markers=True,
    color_discrete_map={"Chubut": COLOR_CHUBUT, "Jujuy": COLOR_JUJUY},
    labels={"mes": "Mes", "n": "Eventos", "provincia": ""}
)
fig_serie.update_layout(height=350)
fig_serie = aplicar_estilo(fig_serie)

layout = html.Div([
    # 1. Breadcrumbs
    html.Div("Inicio | Trabajo e ingresos | Protestas", className="breadcrumbs"),
    
    html.Div([
        # 2. Título principal
        html.H1("Panorama de las protestas"),
        
        # 3. Texto introductorio
        html.P(
            "Este análisis compara dos ciclos de protesta fundamentales en la Argentina reciente: "
            "el conflicto por la ley de zonificación minera en Chubut (octubre 2021 - enero 2022) "
            "y el conflicto por la reforma constitucional en Jujuy (junio - agosto 2023). "
            "El objetivo es observar cómo reaccionó el Estado provincial frente a cada caso."
        ),
        
        # 4. Sección de Mensajes Clave (Estilo Argendata)
        html.Div([
            html.H4("Mensajes clave", className="mensajes-clave-title"),
            dbc.Row([
                dbc.Col(html.Div("Chubut registró 121 eventos, casi el doble que Jujuy (66).", className="mensaje-card"), width=3),
                dbc.Col(html.Div("La represión en Jujuy fue más intensa: 7,6% de los eventos, contra 4,1% en Chubut.", className="mensaje-card destacado"), width=3),
                dbc.Col(html.Div("El corte de ruta fue el repertorio más castigado en ambas provincias.", className="mensaje-card"), width=3),
                dbc.Col(html.Div("Los eventos de Jujuy fueron más densos: 1,48 demandas por evento vs 0,95.", className="mensaje-card"), width=3),
            ])
        ], className="mensajes-clave-wrapper"),
        
        # 5. El Gráfico enmarcado (Estilo Argendata)
        html.Div([
            html.Div([
                html.P("Eventos por mes", className="chart-title"),
                html.Div("⬇️ ⛶", style={"color": "#999", "fontSize": "14px"}) # Simulación de botones
            ], className="chart-header"),
            html.P("Evolución de la cantidad de eventos registrados por mes en cada provincia.", className="chart-subtitle"),
            html.Div(dcc.Graph(figure=fig_serie, config={'displayModeBar': False}), className="chart-body"),
            html.Div("Fuente: Base propia de eventos codificados a partir de noticias.", className="chart-footer")
        ], className="chart-container"),
        
        # 6. Hallazgo final
        html.Div([
            html.H5("El hallazgo central"),
            html.P("Chubut optó por la desescalada política (derogación de la ley), mientras que Jujuy "
                   "sostuvo una estrategia de disciplinamiento (mantener la reforma y reprimir).")
        ], className="hallazgo-box"),

        # 7. Botones de navegación
        html.Div([
            dcc.Link("← Volver al inicio", href="/", className="btn btn-outline-secondary"),
            dcc.Link("Siguiente: Repertorios →", href="/repertorios", className="btn btn-primary float-end"),
        ], style={"marginTop": "40px", "overflow": "hidden"}),
        
    ], className="page-container")
])