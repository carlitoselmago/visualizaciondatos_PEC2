import os
import kagglehub
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pycountry

# ID del dataset en Kaggle
dataset_id = "marchman/geo-nuclear-data"
nombre_archivo = "data/csv/raw/4-nuclear_power_plants.csv"

# Descarga el dataset (usa la caché local si ya está)
ruta_dataset = kagglehub.dataset_download(dataset_id)
ruta_csv = os.path.join(ruta_dataset, nombre_archivo)

if not os.path.exists(ruta_csv):
    raise FileNotFoundError(f"No se encontró el archivo dentro del dataset: {ruta_csv}")

# Leer CSV con separador ;
df = pd.read_csv(ruta_csv, sep=";")

# Normalizar los códigos de país (⚙️ esta línea es la que corrige tu problema)
df["CountryCode"] = df["CountryCode"].astype(str).str.strip().str.upper()

# Convertir a datetime (maneja errores por seguridad)
df["OperationalFrom"] = pd.to_datetime(df["OperationalFrom"], errors="coerce")
df["OperationalTo"] = pd.to_datetime(df["OperationalTo"], errors="coerce")

pd.set_option("display.max_columns", None)

today = pd.Timestamp.today()

# Calcular si está operativo
df["is_operational"] = (
    df["OperationalFrom"].notna()
    & ((df["OperationalTo"].isna()) | (df["OperationalTo"] > today))
)
print(df.head())


# Agrupar por país
summary = (
    df.groupby("CountryCode")
    .agg(
        total_powerplants=("Name", "count"),
        operational_powerplants=("is_operational", "sum"),
    )
    .reset_index()
)

# Añadir nombre del país
def code_to_name(code):
    try:
        return pycountry.countries.get(alpha_2=code).name
    except:
        return None



# Ordenar por número total de plantas
summary = summary.sort_values("total_powerplants", ascending=False)

top10=summary.head(10)
print(top10)
"""

"""
countries_list=top10.CountryCode.values

df2 = df[df.CountryCode.isin(countries_list)]

# Ordenar primero por país (según lista) y luego por operatividad
df2["CountryCode"] = pd.Categorical(df2["CountryCode"], categories=countries_list, ordered=True)
df2["CountryName"] = df2["CountryCode"].apply(code_to_name)

df2 = df2.sort_values(
    by=["CountryCode", "is_operational"],
    ascending=[True, False]  # país ascendente (según lista), operativas primero
).reset_index(drop=True)

print(df2.head())

df2=df2[["CountryName","CountryCode","is_operational","OperationalFrom"]]

df2['is_operational']=df2['is_operational'].astype(str)
df2.loc[df2['is_operational'] == 'True', 'is_operational'] = 'Operativa'
df2.loc[df2['is_operational'] == 'False', 'is_operational'] = 'No operativa'
df2["amount"]=1


df2.to_csv("df/grupo2.csv")


summary.to_csv("df/grupo2_sumario.csv")