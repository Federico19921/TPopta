import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/metodos", name="Métodos")

layout = html.Div([
    html.H1("Notas metodológicas"),
    html.P("Definiciones, limitaciones y decisiones del trabajo.",
           className="text-muted mb-5"),

    html.H2("Fuente de datos"),
    html.P("Base propia de eventos codificados a partir de noticias. "
           "La base de Chubut fue construida con asistencia de un modelo de lenguaje "
           "de gran escala (Groq), con un prompt que replicaba el libro de códigos "
           "utilizado en Jujuy. La base de Jujuy fue provista por la cátedra "
           "y codificada manualmente."),

    html.H2("Definición de protesta"),
    html.P("Se utilizó la definición de acción contenciosa de Tilly y Tarrow (2015). "
           "Se incluyeron únicamente las noticias que reportaban un hecho ocurrido. "
           "Se excluyeron anuncios de protestas futuras, notas de opinión y artículos "
           "que no describían una acción concreta."),

    html.H2("Definición de represión"),
    html.P("Se considera represión a los eventos con subtipos 'Protest with intervention' "
           "o 'Excessive force against protesters', o con uso de fuerza confirmado. "
           "Se distingue de otras formas de intervención estatal como monitoreo, "
           "contención o disuasión."),

    html.H2("Limitaciones"),
    html.Ul([
        html.Li("La codificación con LLM introduce un riesgo de error que no está "
                "presente en la codificación manual. Se revisaron manualmente 20 de "
                "los 121 eventos y se detectaron casos de alucinación."),
        html.Li("La diferencia de tamaño entre los corpus (121 vs 66 eventos) se abordó "
                "utilizando comparaciones relativas."),
        html.Li("La cobertura de la respuesta estatal es desigual. Chubut tiene 24,8% "
                "de eventos sin datos; Jujuy tiene 19,7%. La tasa ajustada por cobertura "
                "corrige parcialmente este sesgo."),
    ]),

    html.H2("Uso de ACLED"),
    html.P("Se consultó ACLED para el período 2020-2024. Solo se encontraron 8 eventos "
           "de represión para Chubut y Jujuy combinadas, todos ya presentes en la base "
           "propia. Se optó por usar la base propia como fuente principal y mencionar "
           "ACLED únicamente como contexto nacional."),

    html.Div([
        dcc.Link("← Volver al inicio", href="/", className="btn btn-outline-secondary"),
    ], style={"marginTop": "32px"}),

], className="page-container")