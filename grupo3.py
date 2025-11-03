import os
import kagglehub
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pycountry

# ID del dataset en Kaggle
dataset_id = "mexwell/us-smoking-trend"
nombre_archivo = "smoking.csv"

# Descarga el dataset (usa la caché local si ya está)
ruta_dataset = kagglehub.dataset_download(dataset_id)
ruta_csv = os.path.join(ruta_dataset, nombre_archivo)

if not os.path.exists(ruta_csv):
    raise FileNotFoundError(f"No se encontró el archivo dentro del dataset: {ruta_csv}")

# Leer CSV con separador ;
df = pd.read_csv(ruta_csv)


pd.set_option("display.max_columns", None)




# Definimos un listado de paises cercanos a España
countries_list = [
    "Spain",
   "Portugal",
    "France",
    "Andorra",
    "Morocco",
    "Belgium",
    "Germany",
    "Italy",
    "United Kingdom"
]

# Filtramos los datos por estos paises
df = df[df.Country.isin(countries_list)]

# Crear tabla pivot
df_pivot = df.pivot_table(
    index="Year",
    columns="Country",
    values="Data.Percentage.Total"
).reset_index()

# Reordenar columnas según la lista original
ordered_cols = ["Year"] + [c for c in countries_list if c in df_pivot.columns]
df_pivot = df_pivot[ordered_cols]




df_pivot=df_pivot.rename(columns={"Year":"Año"}  )

print(df_pivot.head())

df_pivot.to_csv("df/grupo3.csv")