
import pandas as pd
import requests
import time
import logging
import os

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Tu API Key de OpenCage (reemplazar por la tuya)
API_KEY = "TU_API_KEY_AQUI"

# Ruta del archivo
archivo = "D:/NSERV/RetailAR Proyecto/00.Data/provincias_ciudades_con_coords.csv"

# Validar existencia
if not os.path.exists(archivo):
    logging.error(f"No se encontró el archivo: {archivo}")
    exit()

# Leer archivo
df = pd.read_csv(archivo)
df["latitud"] = None
df["longitud"] = None

exitos = 0
fallidos = 0

# Geocodificación con OpenCage
for i, row in df.iterrows():
    lugar = f"{row['ciudad']}, {row['provincia_nombre']}, Argentina"
    url = f"https://api.opencagedata.com/geocode/v1/json?q={lugar}&key={API_KEY}&language=es&limit=1"
    try:
        response = requests.get(url)
        data = response.json()
        if data["results"]:
            coords = data["results"][0]["geometry"]
            df.at[i, "latitud"] = coords["lat"]
            df.at[i, "longitud"] = coords["lng"]
            logging.info(f"✔️ {lugar} → lat: {coords['lat']}, lon: {coords['lng']}")
            exitos += 1
        else:
            logging.warning(f"❌ No se encontró: {lugar}")
            fallidos += 1
    except Exception as e:
        logging.error(f"Error en {lugar}: {e}")
        fallidos += 1
    time.sleep(1)

# Guardar resultados
salida = "D:/NSERV/RetailAR Proyecto/00.Data/provincias_ciudades_con_coords_completo.csv"
df.to_csv(salida, index=False)
logging.info(f"✅ Archivo generado: {salida}")
logging.info(f"📊 Total: {len(df)} | Éxitos: {exitos} | Fallidos: {fallidos}")
