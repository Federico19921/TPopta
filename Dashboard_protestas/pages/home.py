import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/", name="Inicio")

def card_tema(titulo, descripcion, href, color):
    return dbc.Col(
        dcc.Link(
            dbc.Card([
                dbc.CardBody([
                    html.Div(style={
                        "width": "40px",
                        "height": "4px",
                        "backgroundColor": color,
                        "marginBottom": "16px",
                        "borderRadius": "2px"
                    }),
                    html.H5(titulo),
                    html.P(descripcion, className="text-muted mb-0",
                           style={"fontSize": "0.85rem"})
                ])
            ], style={"height": "100%"}),
            href=href,
            className="tema-card"
        ),
        width=6,
        className="mb-4"
    )

layout = html.Div([
    html.H1("Protestas en Chubut y Jujuy"),
    html.P(
        "Un análisis comparado de dos ciclos de protesta y la respuesta estatal. "
        "Chubut (oct 2021 - ene 2022) y Jujuy (jun - ago 2023).",
        className="text-muted mb-5"
    ),

    html.H2("Explorá el análisis"),

    dbc.Row([
        card_tema("Panorama general",
                  "KPIs, serie temporal y contexto de los dos conflictos.",
                  "/panorama", "#7BB4C2"),
        card_tema("Repertorios y actores",
                  "Qué se hizo y quiénes lo hicieron en cada provincia.",
                  "/repertorios", "#9D9ECE"),
        card_tema("Demandas",
                  "Qué se reclamó y cómo se articuló en cada caso.",
                  "/demandas", "#2E86AB"),
        card_tema("Cruces",
                  "Actores × demandas × represión. El corazón del comparativo.",
                  "/cruces", "#A23B72"),
        card_tema("Represión",
                  "Intervención estatal, corte de ruta y selectividad represiva.",
                  "/represion", "#E53935"),
        card_tema("Métodos",
                  "Definiciones, limitaciones y uso de ACLED.",
                  "/metodos", "#6B7280"),
    ]),

], className="page-container")