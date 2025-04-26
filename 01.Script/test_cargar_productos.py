
import pandas as pd
from sqlalchemy import create_engine
import os

# Ruta del archivo
archivo = "D:/NSERV/RetailAR Proyecto/00.Data/Productos.csv"

# Validar si el archivo existe
if not os.path.exists(archivo):
    print(f"❌ Archivo no encontrado: {archivo}")
    exit()

# Leer CSV
df = pd.read_csv(archivo)
print(f"📦 Archivo leído correctamente: {len(df)} filas")

# Mostrar primeras 3 filas
print(df.head(3))

# Crear conexión
try:
    engine = create_engine(
        "mssql+pyodbc://localhost/RetailAR?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
    )
    print("✅ Conexión a SQL Server exitosa")

    # Cargar solo 5 filas
    df.head(5).to_sql("DimProducto", schema="ventas", con=engine, if_exists="append", index=False)
    print("🚀 5 productos cargados a ventas.DimProducto")

except Exception as e:
    print(f"❌ Error de conexión o carga: {e}")
