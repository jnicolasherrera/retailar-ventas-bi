
import pandas as pd
from sqlalchemy import create_engine

# Leer el archivo CSV con coordenadas
df = pd.read_csv("D:/NSERV/RetailAR Proyecto/00.Data/provincias_ciudades_con_coords.csv")

# Crear conexión a SQL Server
server = "localhost"
database = "RetailAR"
engine = create_engine(
    f"mssql+pyodbc://{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
)

# Cargar los datos a la tabla ventas.DimLocalidad
df.to_sql("DimLocalidad", schema="ventas", con=engine, if_exists="append", index=False)

print("✅ provincias_ciudades_con_coords.csv cargado a ventas.DimLocalidad con éxito.")
