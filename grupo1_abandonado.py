import os
import kagglehub
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ID del dataset en Kaggle
dataset_id = "benantolin/joker2data"

# Nombre del archivo Excel dentro del dataset
nombre_archivo = "Joker2_reviews.xlsx"

# Descarga el dataset (usa la caché local si ya está)
ruta_dataset = kagglehub.dataset_download(dataset_id)

# Ruta completa al archivo Excel
ruta_xlsx = os.path.join(ruta_dataset, nombre_archivo)

# Comprobamos que el archivo exista dentro de la carpeta descargada
if not os.path.exists(ruta_xlsx):
    raise FileNotFoundError(f"No se encontró el archivo dentro del dataset: {ruta_xlsx}")

# Leemos el archivo Excel
df = pd.read_excel(ruta_xlsx)


# --- Convertimos la columna UserRating a valor numérico ---
def convertir_rating(r):
    if pd.isna(r):  # Si hay valores vacíos
        return None
    r = str(r).strip()
    estrellas = r.count('★')
    medio = 0.5 if '½' in r else 0
    return estrellas + medio

df['UserRating'] = df['UserRating'].apply(convertir_rating)

df["ReviewLength"] = df["Review"].str.len()

print(df.head())


df.to_excel("df/grupo1.xlsx")  



# --- Agrupamos la longitud en bins de 50 ---
bin_size = 50
df["ReviewLength_binned"] = (df["ReviewLength"] // bin_size) * bin_size

# --- Hacemos el scatter usando los valores binned ---
plt.figure(figsize=(8, 6))
plt.scatter(
    df["UserRating"],
    df["ReviewLength_binned"],
    alpha=0.1,
    s=30,
    color='blue',
    edgecolors='none'
)

plt.title("Densidad entre puntuación y longitud de la reseña (agrupada cada 50 caracteres)")
plt.xlabel("Puntuación del usuario (UserRating)")
plt.ylabel("Longitud de la reseña (caracteres, agrupada)")
plt.grid(True, linestyle='--', alpha=0.4)
plt.show()