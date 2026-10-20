import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import folium
from folium import plugins
import pandas as pd
import numpy as np

# ---------- Datos de juguete ----------
np.random.seed(42)

ciudades = {
    "Madrid":   {"lat": 40.4168, "lon": -3.7038},
    "Barcelona":{"lat": 41.3874, "lon":  2.1686},
    "Sevilla":  {"lat": 37.3891, "lon": -5.9845},
    "Bilbao":   {"lat": 43.2630, "lon": -2.9350},
}

meses = ["Ene", "Feb", "Mar", "Abr", "May", "Jun",
         "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]

# Generamos temperaturas ficticias por ciudad
rows = []
for ciudad in ciudades:
    base = np.random.randint(12, 20)
    for i, mes in enumerate(meses):
        temp = base + 10 * np.sin((i - 3) / 12 * 2 * np.pi) + np.random.normal(0, 1.5)
        rows.append({"Ciudad": ciudad, "Mes": mes, "Temperatura": round(temp, 1)})

df = pd.DataFrame(rows)

# ---------- App ----------
app = dash.Dash(__name__)

app.layout = html.Div(
    style={"fontFamily": "Arial, sans-serif", "padding": "20px"},
    children=[
        html.H1("🌤️ Dashboard del Clima (ejemplo de juguete)"),
        html.P("Selecciona una ciudad para ver su gráfico y su mapa."),

        dcc.Dropdown(
            id="selector-ciudad",
            options=[{"label": c, "value": c} for c in ciudades],
            value="Madrid",
            clearable=False,
            style={"width": "300px", "marginBottom": "20px"},
        ),

        html.Div(
            style={"display": "flex", "gap": "30px", "flexWrap": "wrap"},
            children=[
                dcc.Graph(id="grafico-temperatura", style={"flex": "1", "minWidth": "400px"}),
                html.Iframe(
                    id="mapa-folium",
                    style={"flex": "1", "minWidth": "400px", "height": "500px",
                           "border": "1px solid #ccc", "borderRadius": "8px"},
                ),
            ],
        ),
    ],
)


# ---------- Callbacks ----------
@app.callback(
    Output("grafico-temperatura", "figure"),
    Output("mapa-folium", "srcDoc"),
    Input("selector-ciudad", "value"),
)
def actualizar(ciudad):
    # --- Gráfico Plotly ---
    df_ciudad = df[df["Ciudad"] == ciudad]
    fig = px.line(
        df_ciudad, x="Mes", y="Temperatura",
        title=f"Temperatura media mensual en {ciudad}",
        markers=True,
    )
    fig.update_layout(
        yaxis_title="Temperatura (°C)",
        xaxis_title="",
        template="plotly_white",
    )

    # --- Mapa Folium ---
    coords = ciudades[ciudad]
    mapa = folium.Map(location=[coords["lat"], coords["lon"]], zoom_start=11)

    folium.Marker(
        [coords["lat"], coords["lon"]],
        popup=f"<b>{ciudad}</b>",
        tooltip=ciudad,
        icon=folium.Icon(color="blue", icon="info-sign"),
    ).add_to(mapa)

    # Añadimos un pequeño círculo para que se vea algo más
    folium.Circle(
        [coords["lat"], coords["lon"]],
        radius=3000,
        color="crimson",
        fill=True,
        fill_opacity=0.15,
    ).add_to(mapa)

    # Convertimos el mapa a HTML para incrustarlo en un iframe
    mapa_html = mapa._repr_html_()

    return fig, mapa_html


if __name__ == "__main__":
    app.run(debug=True)