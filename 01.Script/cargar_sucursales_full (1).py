
import pandas as pd
from sqlalchemy import create_engine, text

archivo = "D:/NSERV/RetailAR Proyecto/00.Data/Sucursales.csv"
df = pd.read_csv(archivo)

engine = create_engine(
    "mssql+pyodbc://localhost/RetailAR?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
)

with engine.connect() as conn:
    conn.execute(text("DELETE FROM ventas.DimSucursal"))
    conn.commit()

df.to_sql("DimSucursal", schema="ventas", con=engine, if_exists="append", index=False)
print(f"✅ Sucursales cargadas: {len(df)} filas")
