
import pandas as pd
from sqlalchemy import create_engine

# Leer el archivo tipo_cambio.csv (ajustar la ruta si lo movés)
df = pd.read_csv("D:/NSERV/RetailAR Proyecto/00.Data/tipo_cambio.csv")

# Crear cadena de conexión a SQL Server
server = "localhost"
database = "RetailAR"
engine = create_engine(
    f"mssql+pyodbc://{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
)

# Cargar los datos a la tabla ventas.DimTipoCambio
df.to_sql("DimTipoCambio", schema="ventas", con=engine, if_exists="append", index=False)

print("✅ tipo_cambio.csv cargado a ventas.DimTipoCambio con éxito.")
