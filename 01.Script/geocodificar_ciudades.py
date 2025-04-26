
import pandas as pd
from geopy.geocoders import Nominatim
import time

# Leer archivo con provincias y ciudades
pd.read_csv("D:/NSERV/RetailAR Proyecto/00.Data/provincias_ciudades_con_coords.csv")


# Inicializar geolocalizador
geolocator = Nominatim(user_agent="geoapi_exercise")

# Agregar columnas vacías
df["latitud"] = None
df["longitud"] = None

# Geolocalizar cada ciudad
for i, row in df.iterrows():
    lugar = f"{row['ciudad']}, {row['provincia_nombre']}, Argentina"
    try:
        location = geolocator.geocode(lugar, timeout=10)
        if location:
            df.at[i, "latitud"] = location.latitude
            df.at[i, "longitud"] = location.longitude
        else:
            print(f"No se encontró: {lugar}")
    except Exception as e:
        print(f"Error en {lugar}: {e}")
    time.sleep(1)  # evitar bloqueo por rate limit

# Guardar el nuevo archivo
df.to_csv("provincias_ciudades_con_coords.csv", index=False)
print("✅ Archivo generado: provincias_ciudades_con_coords.csv")
