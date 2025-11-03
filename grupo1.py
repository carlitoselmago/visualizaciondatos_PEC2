import os
import kagglehub
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pycountry

# ID del dataset en Kaggle
dataset_id = "whigmalwhim/steam-releases"
nombre_archivo = "game_data_all.csv"

# Descarga el dataset (usa la caché local si ya está)
ruta_dataset = kagglehub.dataset_download(dataset_id)
ruta_csv = os.path.join(ruta_dataset, nombre_archivo)

if not os.path.exists(ruta_csv):
    raise FileNotFoundError(f"No se encontró el archivo dentro del dataset: {ruta_csv}")

# Leer CSV con separador ;
df = pd.read_csv(ruta_csv)


pd.set_option("display.max_columns", None)

columns=["game","total_reviews","rating","primary_genre","peak_players"]

df=df[columns]


def limpiargenre(r):
    r = str(r).strip()
    p= r.split(" ")
    return p[0]


# Eliminamos juegos que no tengan un mínimo de 100 jugadores
df = df[(df.peak_players > 100)]

# Filtramos las categorias para que solo conste el nombre
df["primary_genre"]=df["primary_genre"].apply(limpiargenre)

# Normalizamos la cantidad de reviews por peak de jugadores
df["avg_reviews"] = df["total_reviews"] / df["peak_players"]

# Tomamos una muestra aleatoria
#df=df.head(5000)
df=df.sample(n=1000)

print(df.head())

df.to_csv("df/grupo1.csv")