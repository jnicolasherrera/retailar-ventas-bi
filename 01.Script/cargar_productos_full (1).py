
import pandas as pd
from sqlalchemy import create_engine, text

archivo = "D:/NSERV/RetailAR Proyecto/00.Data/Productos.csv"
df = pd.read_csv(archivo)

engine = create_engine(
    "mssql+pyodbc://localhost/RetailAR?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
)

with engine.connect() as conn:
    conn.execute(text("DELETE FROM ventas.DimProducto"))
    conn.commit()

df.to_sql("DimProducto", schema="ventas", con=engine, if_exists="append", index=False)
print(f"✅ Productos cargados: {len(df)} filas")
