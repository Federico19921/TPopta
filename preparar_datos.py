import pandas as pd

df = pd.read_excel('../TP Opta/data/processed/eventos_chubut_jujuy.xlsx')

df["noticia_id"] = df["noticia_id"].astype(str)
df["mes"] = df["noticia_id"].str[:6]
df["fecha"] = pd.to_datetime(df["noticia_id"].str[:8], format="%Y%m%d", errors="coerce")

df["escala"] = df["escala"].astype(str).str.lower().str.strip().replace({
    "alta": "alta", "media": "media", "baja": "baja",
    "muy alta": "muy_alta", "no especificado": "99",
    "sin datos": "99", "nan": "99", "99.0": "99", "no aplica": "99"
})

df["intensidad"] = df["intensidad"].astype(str).str.lower().str.strip().replace({
    "alta": "alta", "media": "media", "baja": "baja",
    "muy alta": "muy_alta", "no especificado": "99",
    "sin datos": "99", "nan": "99", "99.0": "99"
})

def armonizar(row):
    prov = row["provincia"]
    cod = row["tipo_intervencion_estatal"]
    if pd.isna(cod): return "Sin datos"
    cod = int(cod)
    if cod == 0: return "Ausencia"
    elif cod == 1: return "Monitoreo"
    elif cod == 2: return "Contención"
    elif cod == 3: return "Represión" if prov == "Chubut" else "Disuasión"
    elif cod == 4: return "Represión"
    else: return "Sin datos"

df["intervencion_armonizada"] = df.apply(armonizar, axis=1)
df["es_represion"] = (df["intervencion_armonizada"] == "Represión").astype(int)

COLS_ACTORES = ["docentes", "gremios_estatales", "sindicatos_privados",
                "organizaciones_sociales", "comunidades_indigenas", "vecinos",
                "colectivos_ambientales", "colectivos_especificos",
                "partidos_politicos", "policias_actores",
                "publico_general", "colectivos_violentos", "otros"]

COLS_DEMANDAS = ["demanda_salarial", "demanda_laboral", "demanda_ambiental_territorial",
                 "demanda_politica_legal", "demanda_ddhh", "demanda_servicios",
                 "demanda_derechos_especificos", "demanda_institucional",
                 "demanda_conmemoracion"]

df["n_actores"] = df[COLS_ACTORES].sum(axis=1)
df["n_demandas"] = df[COLS_DEMANDAS].sum(axis=1)

df.to_csv("Dashboard_protestas/data/eventos.csv", index=False)
print("datos guardados")