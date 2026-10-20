import dash
import dash_bootstrap_components as dbc
from dash import html

app = dash.Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap"
    ],
    suppress_callback_exceptions=True,
    title="Protestas en Chubut y Jujuy"
)

server = app.server  # crítico para Render

navbar = dbc.NavbarSimple(
    brand="Protestas en Chubut y Jujuy",
    brand_href="/",
    color="white",
    dark=False,
    children=[
        dbc.NavItem(dbc.NavLink("Panorama", href="/panorama")),
        dbc.NavItem(dbc.NavLink("Repertorios", href="/repertorios")),
        dbc.NavItem(dbc.NavLink("Demandas", href="/demandas")),
        dbc.NavItem(dbc.NavLink("Cruces", href="/cruces")),
        dbc.NavItem(dbc.NavLink("Represión", href="/represion")),
        dbc.NavItem(dbc.NavLink("Métodos", href="/metodos")),
    ],
    style={"borderBottom": "1px solid #E5E7EB"}
)

app.layout = html.Div([
    navbar,
    dash.page_container
])

if __name__ == "__main__":
    app.run(debug=True, port=8050)