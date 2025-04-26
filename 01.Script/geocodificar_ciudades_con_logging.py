
import pandas as pd
from geopy.geocoders import Nominatim
import time
import logging
import os

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Ruta del archivo de entrada
archivo = "D:/NSERV/RetailAR Proyecto/00.Data/provincias_ciudades_con_coords.csv"

# Verificar si el archivo existe
if not os.path.exists(archivo):
    logging.error(f"No se encontró el archivo: {archivo}")
    exit()

# Cargar el archivo CSV
df = pd.read_csv(archivo)

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
            logging.info(f"✔️ {lugar} → lat: {location.latitude}, lon: {location.longitude}")
        else:
            logging.warning(f"❌ No se encontró: {lugar}")
    except Exception as e:
        logging.error(f"Error geocodificando {lugar}: {e}")
    time.sleep(1)  # evitar bloqueo

# Guardar resultado
salida = "D:/NSERV/RetailAR Proyecto/00.Data/provincias_ciudades_con_coords_completo.csv"
df.to_csv(salida, index=False)
logging.info(f"✅ Archivo generado: {salida}")
